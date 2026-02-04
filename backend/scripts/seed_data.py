"""Seed database with sample data."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from faker import Faker
from datetime import datetime, timedelta
from src.driver.database.connection import AsyncSessionLocal
from src.driver.database.models import UserModel, PostModel, CategoryModel, PostStatusEnum
from src.service.markdown_service import markdown_service
from src.service.auth_service import auth_service

fake = Faker()


async def seed_data():
    """Seed the database with sample data."""
    async with AsyncSessionLocal() as session:
        try:
            # Create admin user
            admin = UserModel(
                username="admin",
                email="admin@example.com",
                hashed_password=auth_service.hash_password("admin123"),
                full_name="Blog Administrator",
                bio="The main author of this blog",
            )
            session.add(admin)
            await session.flush()
            
            # Create categories
            categories = []
            category_names = ["Technology", "Travel", "Food", "Lifestyle", "Tutorial"]
            for name in category_names:
                cat = CategoryModel(
                    name=name,
                    slug=name.lower(),
                    description=f"Posts about {name.lower()}",
                )
                session.add(cat)
                categories.append(cat)
            
            await session.flush()
            
            # Create 10 sample posts
            for i in range(10):
                title = fake.sentence(nb_words=6).rstrip('.')
                slug = title.lower().replace(' ', '-').replace(',', '')[:50]
                
                # Generate Markdown content
                markdown_content = f"""# {title}

{fake.paragraph(nb_sentences=3)}

## Introduction

{fake.paragraph(nb_sentences=5)}

## Main Content

{fake.paragraph(nb_sentences=7)}

### Key Points

- {fake.sentence()}
- {fake.sentence()}
- {fake.sentence()}

## Conclusion

{fake.paragraph(nb_sentences=4)}

---

*Published on {fake.date()}*
"""
                
                html_content = markdown_service.render(markdown_content)
                excerpt = markdown_service.generate_excerpt(markdown_content)
                
                # Random publish date in the past
                days_ago = fake.random_int(min=1, max=90)
                published_at = datetime.utcnow() - timedelta(days=days_ago)
                
                post = PostModel(
                    title=title,
                    slug=slug,
                    content_markdown=markdown_content,
                    content_html=html_content,
                    excerpt=excerpt,
                    status=PostStatusEnum.PUBLISHED,
                    author_id=admin.id,
                    published_at=published_at,
                )
                
                # Add 1-3 random categories
                num_categories = fake.random_int(min=1, max=3)
                post.categories = fake.random_elements(
                    elements=categories,
                    length=num_categories,
                    unique=True,
                )
                
                session.add(post)
            
            await session.commit()
            print("✅ Database seeded successfully!")
            print(f"   - Created 1 admin user (username: admin, password: admin123)")
            print(f"   - Created {len(categories)} categories")
            print(f"   - Created 10 published posts")
            
        except Exception as e:
            await session.rollback()
            print(f"❌ Error seeding database: {e}")
            raise


if __name__ == "__main__":
    print("🌱 Seeding database...")
    asyncio.run(seed_data())
