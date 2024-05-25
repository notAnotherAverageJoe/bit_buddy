import subprocess

def seed_database():
    try:
        subprocess.run(["psql", "-d", "bitbuddy", "-U", "joseph", "-f", "/home/joseph/bit_buddy/capstone-project-one-72bcfbfc8e064f9988d6b18a0eb62373/seed.sql"])
        print("Database seeded successfully!")
    except Exception as e:
        print("Error while seeding the database:", e)

if __name__ == "__main__":
    seed_database()
