from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 's3cr3t_k3y'  # Necessário para o uso de flash messages

# Banco de dados simulado
tasks = []

@app.route("/")
def index():
    """Página inicial que lista todas as tarefas."""
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    """Adiciona uma nova tarefa."""
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        emoji = request.form.get("emoji", "📘")
        
        # Validação simples
        if title:
            task_id = len(tasks) + 1  # Atribui um ID único para a tarefa
            task = {
                "id": task_id,
                "title": title,
                "description": description,
                "emoji": emoji
            }
            tasks.append(task)
            flash("Tarefa adicionada com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("O título da tarefa é obrigatório.", "danger")
    
    return render_template("add_task.html", tasks=tasks)


@app.route("/task/<int:task_id>", methods=["GET", "POST"])
def task_detail(task_id):
    """Exibe os detalhes da tarefa e permite edição."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        flash("Tarefa não encontrada!", "danger")
        return redirect(url_for("index"))

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        emoji = request.form.get("emoji", task["emoji"])

        if title:
            task["title"] = title
            task["description"] = description
            task["emoji"] = emoji
            flash("Tarefa atualizada com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("O título da tarefa é obrigatório.", "danger")

    return render_template("task_detail.html", task=task, tasks=tasks)  # Adicionei tasks aqui


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Exclui uma tarefa."""
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    flash("Tarefa excluída com sucesso!", "success")
    return redirect(url_for("index"))

@app.route("/toggle-theme", methods=["POST"])
def toggle_theme():
    """Altera o tema (modo claro/escuro)."""
    # Para simplificar, não estamos armazenando o tema entre as sessões.
    flash("Tema alternado!", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
