from config import app, db
from models import User, Journal

with app.app_context():
    print("Deleting existing records...")
    User.query.delete()
    Journal.query.delete()

    print("Creating users...")
    user1 = User(username="james")
    user1.password_hash = "james123"

    user2 = User(username="mary")
    user2.password_hash = "maryabc"

    print("Committing users to db...")
    db.session.add_all([user1, user2])
    db.session.commit()

    print("Creating journals...")
    journal1 = Journal(title="my first journal, james", content="Finalized the Q2 roadmap. Action items: update onboarding guide, schedule stakeholder sync, and review vendor contract by next Friday.", user_id=1)
    journal2 = Journal(title="my second journal, james", content="Finalized the Q2 roadmap. Action items: update onboarding guide, schedule stakeholder sync, and review vendor contract by next Friday.", user_id=1)

    journal3 = Journal(title="my first journal, mary", content="Finalized the Q2 roadmap. Action items: update onboarding guide, schedule stakeholder sync, and review vendor contract by next Friday.", user_id=2)
    journal4 = Journal(title="my second journal, mary", content="Finalized the Q2 roadmap. Action items: update onboarding guide, schedule stakeholder sync, and review vendor contract by next Friday.", user_id=2)
    journal5 = Journal(title="my third journal, mary", content="Finalized the Q2 roadmap. Action items: update onboarding guide, schedule stakeholder sync, and review vendor contract by next Friday.", user_id=2)

    print("Committing journals to db...")
    db.session.add_all([journal1, journal2, journal3, journal4, journal5])
    db.session.commit()

    print("Complete...")