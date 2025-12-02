import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STUDENTS_PATH = os.path.join(DATA_DIR, "students.txt")
ASSIGNMENTS_PATH = os.path.join(DATA_DIR, "assignments.txt")
SUBMISSIONS_DIR = os.path.join(DATA_DIR, "submissions")

def load_students():
    students = {}
    with open(STUDENTS_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        for i in range(0, len(lines), 2):
            name = lines[i]
            sid = lines[i+1]
            students[sid] = name
    return students

def load_assignments():
    assignments = {}
    with open(ASSIGNMENTS_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        for i in range(0, len(lines), 3):
            title = lines[i]
            aid = lines[i+1]
            points = int(lines[i+2])
            assignments[aid] = (title, points)
    return assignments

def load_submissions():
    subs = {}
    for filename in os.listdir(SUBMISSIONS_DIR):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(SUBMISSIONS_DIR, filename), "r") as f:
            line = f.readline().strip()
            parts = line.split("|")
            if len(parts) != 3:
                continue
            sid, aid, score = parts
            score = float(score)
            if aid not in subs:
                subs[aid] = {}
            subs[aid][sid] = score
    return subs

def student_grade(students, assignments, subs):
    name = input("What is the student's name: ")
    sid = None
    for k, v in students.items():
        if v.lower() == name.lower():
            sid = k
            break
    if sid is None:
        print("0%")
        return
    total = 0
    earned = 0
    for aid, (title, pts) in assignments.items():
        total += pts
        if aid in subs and sid in subs[aid]:
            s = subs[aid][sid]
            if s <= pts:
                earned += s
    if total == 0:
        print("0%")
    else:
        print(f"{round((earned/total)*100)}%")

def assignment_statistics(assignments, subs):
    title = input("What is the assignment name: ")
    aid = None
    for k,(t,p) in assignments.items():
        if t.lower() == title.lower():
            aid = k
            break
    if aid is None:
        print("Assignment not found")
        return
    scores = []
    if aid in subs:
        for s in subs[aid].values():
            scores.append(s)
    if not scores:
        print("No submissions")
        return
    mn = min(scores)
    mx = max(scores)
    avg = sum(scores)/len(scores)
    print(f"Min: {mn}")
    print(f"Max: {mx}")
    print(f"Avg: {avg:.2f}")

def assignment_graph(assignments, subs):
    title = input("What is the assignment name: ")
    aid = None
    pts = None
    for k,(t,p) in assignments.items():
        if t.lower() == title.lower():
            aid = k
            pts = p
            break
    if aid is None:
        print("Assignment not found")
        return
    scores = []
    if aid in subs:
        for s in subs[aid].values():
            scores.append((s/pts)*100)
    if not scores:
        print("No submissions")
        return
    plt.hist(scores, bins=10)
    plt.title(f"Scores for {title}")
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.show()

def main():
    students = load_students()
    assignments = load_assignments()
    subs = load_submissions()
    while True:
        print("1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        sel = input("Enter your selection: ")
        if sel == "1":
            student_grade(students, assignments, subs)
        elif sel == "2":
            assignment_statistics(assignments, subs)
        elif sel == "3":
            assignment_graph(assignments, subs)
        else:
            break

if __name__ == "__main__":
    main()
