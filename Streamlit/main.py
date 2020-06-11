import sqlite3
import streamlit as st

with sqlite3.connect("TODO.db") as conn:
    curr = conn.cursor()

curr.execute(""" CREATE TABLE IF NOT EXISTS TODOTASK(
    
    taskid INTEGER PRIMARY KEY AUTOINCREMENT,
    task VARCHAR(100) NOT NULL
)""")

def insert_task(tk):
    with conn: #using context manager no need to use commit
        curr.execute("insert into TODOTASK (task) values(?)",(tk,))

def delete_task(id):
    with conn: #using context manager no need to use commit
        curr.execute("DELETE from TODOTASK where taskid = ? ",(id,))

def reset_taskid():
    with conn:
        curr.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'TODOTASK'")

def update_task(tid,new_task):
    with conn:
        curr.execute(""" UPDATE TODOTASK SET task = ?
        WHERE taskid = ?
        """,(new_task,tid))


st.title("TODO APP")
sel = st.sidebar.radio("Navigation",['TASK LIST','DELETE TASK','UPDATE TASK'])
if sel == 'TASK LIST':
    curr.execute('select * from TODOTASK')
    tasks = curr.fetchall()
    print(tasks)
    task = st.text_area("TASK TO ADD",max_chars=100)

    if st.button("ADD TASK"):
        if task.strip() == "":
            st.warning("TASK CAN NOT BE EMPTY")
        else:
            insert_task(task)

    curr.execute('select * from TODOTASK')
    tasks = curr.fetchall()

    
    for t in tasks:
        st.write(f"Task ID:{t[0]} || {t[1]}")

if sel == 'DELETE TASK':
    curr.execute('select * from TODOTASK')
    tasks = curr.fetchall()
    id = st.selectbox("Select the ID to delete",[x[0] for x in tasks],key=1)
    if st.button("DELETE"):
        st.warning("You are about to delete a task")
        delete_task(id)
        reset_taskid()
        st.balloons()

if sel == 'UPDATE TASK':
    curr.execute('select * from TODOTASK')
    tasks = curr.fetchall()
    id = st.selectbox("Select the ID to delete",[x[0] for x in tasks],key=1)
    curr.execute('select * from TODOTASK where taskid = ?',(id,))
    task_req = curr.fetchone()
    new_task = st.text_area("Edit",value=task_req[1])
    if st.button("Save"):
        update_task(task_req[0],new_task)

