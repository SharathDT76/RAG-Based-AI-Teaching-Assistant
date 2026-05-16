async function askQuestion(){

    let question =
        document.getElementById(
            "question"
        ).value;

    let responseDiv =
        document.getElementById(
            "response"
        );

    if(question.trim() === ""){

        return;
    }

    responseDiv.innerHTML = `
        <div class="loader"></div>
    `;

    try{

        let res = await fetch("/ask", {

            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                question:question
            })
        });

        let data = await res.json();

        responseDiv.innerHTML = `
            <div class="ai-response">
                ${data.answer}
            </div>
        `;

    }catch(error){

        responseDiv.innerHTML = `

            <div class="error-box">

                <h2>Error</h2>

                <p>
                    Failed to fetch response.
                </p>

            </div>
        `;
    }
}

/* =========================
   ENTER KEY SEARCH
========================= */

document
.addEventListener(
    "DOMContentLoaded",
    () => {

        document
        .getElementById("question")
        .addEventListener(
            "keypress",
            function(event){

                if(event.key === "Enter"){

                    askQuestion();
                }
            }
        );

        loadTheme();
    }
);

/* =========================
   THEME TOGGLE
========================= */

function toggleTheme(){

    document.body.classList.toggle(
        "dark"
    );

    let btn =
        document.getElementById(
            "themeToggle"
        );

    if(
        document.body.classList.contains(
            "dark"
        )
    ){

        btn.innerHTML = "☀️";

        localStorage.setItem(
            "theme",
            "dark"
        );

    }else{

        btn.innerHTML = "🌙";

        localStorage.setItem(
            "theme",
            "light"
        );
    }
}

window.onload = () => {

    let savedTheme =
        localStorage.getItem(
            "theme"
        );

    let btn =
        document.getElementById(
            "themeToggle"
        );

    if(savedTheme === "dark"){

        document.body.classList.add(
            "dark"
        );

        btn.innerHTML = "☀️";

    }else{

        btn.innerHTML = "🌙";
    }
};

/* =========================
   LOAD SAVED THEME
========================= */

function loadTheme(){

    let savedTheme =
        localStorage.getItem(
            "theme"
        );

    let btn =
        document.getElementById(
            "themeToggle"
        );

    if(savedTheme === "dark"){

        document.body.classList.add(
            "dark"
        );

        btn.innerHTML = "☀️";

    }else{

        document.body.classList.remove(
            "dark"
        );

        btn.innerHTML = "🌙";
    }
}