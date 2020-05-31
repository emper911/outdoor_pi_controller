const host = "http://OutdoorController:3000";

const state = {
    power: {
        lights: false,
        pump: false,
        misc: false,
    }
}

const init = () => {
    let powerButtons = Object.keys(state.power).map((source) => {
         return document.getElementById(`${source}`)
    });
    powerButtons.map((source) => {
        source.addEventListener("click", powerButtonHandler)
    });
}

const powerButtonHandler = async (event) => {
    const source = event.target.id;
    const powerStatus = !state.power[source];

    const data = await relaySwitch(source, powerStatus);
    if (data) {
        state.power[source] = data["powerStatus"];
        const button = document.getElementById(source);
        (data[source]) ? 
            button.classList.add("controller-buttons-active")
        :
            button.classList.remove("controller-buttons-active")
    }
}

const relaySwitch = async (source, power) => {
    let url = new URL(host + '/' + source);
    let params = {powerStatus: power };
    url.search = new URLSearchParams(params).toString();
    try{
        const response = await fetch(url);
        return response.json();
    }
    catch(err){
        console.log(err);
        return null;
    }
}

window.addEventListener("load", init);
