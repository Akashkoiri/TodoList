const form = document.getElementById('form')

form.addEventListener('submit', (e)=> {
    let task = e.target.NewTask.value;
    if (validateTask(task)) {
        e.preventDefault()
    }
})


function validateTask(task) {
    if (!!task) {
        for (let i in task) {
            if (task[i] != ' ' && task[i] != '\n') {
                return false
            }
        }
    }
    return true
}
