from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo para validação da tarefa
class Task(BaseModel):
    name: str
    description: str

# Lista para armazenar as tarefas
tasks = []

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    # Verifica se a tarefa já existe
    for existing_task in tasks:
        if existing_task["name"] == task.name:
            raise HTTPException(status_code=400, detail="Task already exists")
    
    # Adiciona a nova tarefa
    task_dict = {"name": task.name, "description": task.description, "completed": False}
    tasks.append(task_dict)
    return task

@app.get("/tasks/", response_model=List[dict])
async def list_tasks():
    return tasks

@app.put("/tasks/{task_name}")
async def complete_task(task_name: str):
    for task in tasks:
        if task["name"] == task_name:
            task["completed"] = True
            return {"message": f"Task '{task_name}' marked as completed"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_name}")
async def delete_task(task_name: str):
    for i, task in enumerate(tasks):
        if task["name"] == task_name:
            tasks.pop(i)
            return {"message": f"Task '{task_name}' deleted"}
    raise HTTPException(status_code=404, detail="Task not found")