from app.models import *

print(User.__tablename__)
print(Project.__tablename__)
print(Queue.__tablename__)
print(RetryPolicy.__tablename__)
print(Job.__tablename__)
print(Worker.__tablename__)
print(ExecutionLog.__tablename__)
print(DeadLetterQueue.__tablename__)

print("\n✅ All models imported successfully.")