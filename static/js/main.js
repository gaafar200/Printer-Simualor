let CurrentTasks = {}
let refillInkButton = document.getElementById("ink");
let paperJamButton = document.querySelector("#paperJam");
let paperButton = document.querySelector("#paper");
let reset = document.querySelector("#resetPrinter")
let warningSectionButton = document.querySelector("#warning");
let warningSection = document.getElementById("warningSection");
let status1 = "idle";
setImmediateInterval(() => {
    getData("http://localhost:5000/data").then(d => {
        if (d.err) {
            handleErrorInPrinter(d.err)
        }
        else {
            data = d.data;
            displayPrinterStatus(data.status);
            displayPrinterInk(data.AmountOfInk);
            displayPaper(data.NumberOfPaper);
            let queue = {}
            data.printingQueue.forEach(e => {
                queue[e.key] = e
            })
            displayPrintingTasks(queue);
            checkForErrors(data.status,data.AmountOfInk,data.NumberOfPaper);
            checkForWarnings(data.status,data.AmountOfInk,data.NumberOfPaper);
        }
    })
}, 500)

function setImmediateInterval(cb, time) {
    cb()
    return setInterval(cb, time)
}
async function getData(url) {
    let res = await fetch(url)
    if (res.ok) {
        let data = await res.json()
        return { err: false, data }
    }
    else {
        return { err: true, message: res.text() }
    }
}

function handleErrorInPrinter(error) {
    //todo
}
function displayPrintingTasks(printingQueue) {
    let sideBarTasks = document.querySelector(".side-bar-tasks");
    Object.values(printingQueue).forEach(element => {
        if (!(element.key in CurrentTasks)) {
            let button = celm({name:"button",classes:["cancel-task"],type:"button",innerText:"cancel"});
            
            let task = celm({name:"div",classes:["task"],innerText:element.status});
            let answer = celm({name:"div",classes:["answer"],innerText:element.value});
            let container = celm({name:"div",classes:["task-container"],childs:[answer,button]});
            let navBar = celm({name:"div",childs:[task,container],classes:["content-container"]});
            button.addEventListener("click",function(){
                cancelTask(navBar,element.key);
            });
            answer.innerText = element.value;
            task.innerText = element.status;
            sideBarTasks.appendChild(navBar);
            task.addEventListener("click", (e) => {
                console.log(e.target.classList);
                if(e.target.classList.contains("active")){
                    task.classList.remove("active");
                    container.classList.remove("collapse");
                    return;
                }
                colabseAllOfThem();
                task.classList.toggle("active");
                container.classList.toggle("collapse");
            }, false);
            CurrentTasks[element.key] = { navBar, task, answer };
        }
    });
    for (key in CurrentTasks) {
        if (!(key in printingQueue)) {
            CurrentTasks[key].navBar.remove()
            delete CurrentTasks[key];
        }
        else {
            CurrentTasks[key]&& (CurrentTasks[key].task.innerText = printingQueue[key].status)
        }

    }
}
function cancelTask(task,key){
    fetch("http://localhost:5000/cancel/" + key).then(res=>{
        if(res.ok){
            task.remove()
        }
    })
}
function celm(obj){
    const element = document.createElement(obj.name);
    obj.classes&&obj.classes.length>0&&(obj.classes.forEach(c=>element.classList.add(c)));
    obj.styles&& (element.style = obj.status);
    obj.childs && (obj.childs.forEach(c=>element.appendChild(c)));
    obj.innerText&&(element.innerText=obj.innerText)
    obj.type && (element.type = obj.type)
    return element;
}

function displayPrinterStatus(status) {
    let statusTag = document.querySelector("#status spam");
    statusTag.innerText = " " + status.toUpperCase();
    if(status == "Paused"){
        displayResumeButton();
    }

    else if(status == "offLine"){
        setOffLineMode();
    }
}
function displayPrinterInk(ink) {
    let inkTag = document.querySelector("#ink spam");
    inkTag.innerText = " " + ink.toFixed(2) + " INK";
}

function displayPaper(NumberOfPaper) {
    let paperTag = document.querySelector("#paper spam")
    paperTag.innerText = " " + NumberOfPaper + " Paper"
}

let offline = document.querySelector('#offline');
let online = document.querySelector('#online');
offline.addEventListener("click", function () {
    post("http://localhost:5000/offline").then(res=>{
        if(res.ok){
            setOffLineMode();
        }
    })
});
online.addEventListener("click", function () {
    post("http://localhost:5000/online").then(res=>{
        console.log("Response: " + res.status);
        if(res.ok){
            setOnLineMode();
        }
    })    
});


/** INFO SECTION */
let errors = document.querySelector("#errors");
let alertError = document.querySelector(".alerts .myalert-danger");
let warning = document.querySelector("#warning");
let alertWarning = document.querySelector(".alerts .myalert-warning");
let info = document.querySelector("#info");
let alertInfo = document.querySelector(".alerts .myalert-info");
errors.addEventListener("click", function () {
    if (alertError.classList.contains("hidden")) {
        alertError.classList.remove("hidden");
    }
    else {
        alertError.classList.add("hidden");
    }
    if (!alertWarning.classList.contains("hidden")) {
        alertWarning.classList.add("hidden");
    }
    if (!alertInfo.classList.contains("hidden")) {
        alertInfo.classList.add("hidden");
    }
});

warning.addEventListener("click", function () {
    if (alertWarning.classList.contains("hidden")) {
        alertWarning.classList.remove("hidden");
    }
    else {
        alertWarning.classList.add("hidden");
    }
    if (!alertError.classList.contains("hidden")) {
        alertError.classList.add("hidden");
    }
    if (!alertInfo.classList.contains("hidden")) {
        alertInfo.classList.add("hidden");
    }
});
info.addEventListener("click", function () {
    if (alertInfo.classList.contains("hidden")) {
        alertInfo.classList.remove("hidden");
    }
    else {
        alertInfo.classList.add("hidden");
    }
    if (!alertError.classList.contains("hidden")) {
        alertError.classList.add("hidden");
    }
    if (!alertWarning.classList.contains("hidden")) {
        alertWarning.classList.add("hidden");
    }
});


/** Pause And Resume Section */
let pause = document.querySelector("#pause");
let resume = document.querySelector("#resume");
pause.addEventListener("click", function () {
    post("http://localhost:5000/pause").then(res=>{
        if(res.ok){
            pause.classList.add("hidden");
            resume.classList.remove("hidden");
        }
    })
});

resume.addEventListener("click", function () {
    post("http://localhost:5000/resume").then(res=>{
        if(res.ok){
            resume.classList.add("hidden");
            pause.classList.remove("hidden");
        }
    })
});

function colabseAllOfThem(tasks) {
   containers = document.querySelectorAll(".task-container")
   tasks = document.querySelectorAll(".task");
    for (let i = 0; i < tasks.length; i++) {
        if (containers[i].classList.contains("collapse")) {
            containers[i].classList.remove("collapse");
            tasks[i].classList.toggle("active");
        }
    }
}
function collabseThisOne(task,button) {
    task.classList.remove("active");
    button.classList.remove("active");
    let content = task.nextElementSibling;
    content.style.maxHeight = 0;
}

 function post(url,data){
    return  fetch(url,{
        method: 'POST',
        body:data
    })
}

let print = document.querySelector(".print");
printCallBackFunction = function(e){
    e.preventDefault()
    console.log(status1)
    if(status1 == "offline"){
        displaySpecificWarning("The Printer Is Currently Offline and can't accept printing requests");
        return;
    }
    let text = document.querySelector(".print .text").value;
    const formdata=new FormData()
    formdata.append("text",text)
    post("http://localhost:5000/print",formdata);
}
print.addEventListener("submit",printCallBackFunction)


function checkForErrors(status,AmountOfInk,AmountOfPaper){
    let errors = [];
    if(status == "paperJam"){
        errors.push({key:"paperJam",value:"A paper Jam Occured Please Fix it to continue printing"});
    }
    else if(status == "outOfPaper"){
        errors.push({key:"outOfPaper",value:"The Printer Is Out Of Paper"});
    }
    else if(status == "outOfInk"){
        errors.push({key:"outOfInk",value:"The printer is out of ink"});
    }
    displayErrors(errors);
}

function displayErrors(errors){
    errors.forEach((error)=>{
        if(error.key == "paperJam"){
            paperJamButton.classList.remove("disabled");
            displaySpecificError(error.value);
            return;
        }
        else if(error.key == "outOfPaper"){
            paperButton.classList.remove("disabled");
            displaySpecificError(error.value);
            return;
        }
        else if(error.key == "outOfInk"){
            refillInkButton.classList.remove("disabled");
            displaySpecificError(error.value);
            return;
        }
    })
    function displaySpecificError(error){
        let errorSection = document.getElementById("error");
        let errorButton = document.getElementById("errors");
        errorButton.classList.remove("disabled");
        errorSection.innerText = error.value;
    }
    refillInkButton.addEventListener("click",()=>{
        post("http://www.localhost:5000/refillInk")
        .then(res=>{
            if(res.ok){
                this.classList.add("disabled");
            }
        });
        
    })
    paperJamButton.addEventListener("click",()=>{
        post("http://www.localhost:5000/fixPaperJam")
        .then(res=>{
            if(res.ok){
                this.classList.add("disabled");
            }
        });
    })
    paperButton.addEventListener("click",function(){
        post("http://www.localhost:5000/refillPaper")
        .then(res=>{
            if(res.ok){
                this.classList.add("diabled");
            }
        });
    });
}

function checkForWarnings(status,amountOfInk,amountOfPaper){
    let warnings = [];
    console.log(amountOfPaper);
    if(amountOfPaper <  40){
        warnings.push({key:"paperWarning",value:"Low A mount Of Paper"});
        paperButton.classList.remove("disabled");
    }
    if(amountOfInk < 400){
        warnings.push({key:"paperWarning",value:"Low A mount Of Paper"});
        refillInkButton.classList.remove("disabled");
    }
    displayWarning(warnings);
}

function displayWarning(warnings){
    warnings.forEach((warning)=>{
        displaySpecificWarning(warning.value);
    })
}
function displaySpecificWarning(warning){

    warningSectionButton.classList.remove("disabled");
    warningSection.innerText = warning;
}

function displayResumeButton(){
    pause.classList.add("hidden");
    resume.classList.remove("hidden");
}


function setOffLineMode(){
    if(pause.classList.contains("hidden")){
        resume.classList.add("disabled");
    }
    pause.classList.add("disabled");
    reset.classList.add("disabled");
    offline.classList.add("hidden");
    online.classList.remove("hidden");
    status1="offline"
}

function setOnLineMode(){
    if(pause.classList.contains("hidden")){
        resume.classList.remove("disabled");
    }
    pause.classList.remove("disabled");
    reset.classList.remove("disabled");
    offline.classList.remove("hidden");
    online.classList.add("hidden");
    if(!warningSectionButton.classList.contains("disabled")){
        warningSectionButton.classList.add("disabled")
    }
    status1 = "online"
}