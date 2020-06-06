// const host = "http://OutdoorController:3000/garden";
const host = "http://localhost:3000/garden";

let state = {
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

// const getServerState = async () => {
//     let url = new URL(host + '/' + 'state')
//     try {
//         const response = await (await fetch(url)).json();
//         console.log(response);
//         return response;
//     }
//     catch (err) {
//         console.log(err);
//         return null;
//     }
// }

const powerButtonHandler = async (event) => {
    const source = event.target.id;
    const powerStatus = !state.power[source];
    console.log(source);
    const data = await relaySwitch(source, powerStatus);
    if (data) {
        state.power[source] = (data["powerStatus"] == "true");
        const button = document.getElementById(source);
        (state.power[source]) ?
            button.classList.add("controller-buttons-active")
        :
            button.classList.remove("controller-buttons-active")
    }
    console.log(state);
}

const relaySwitch = async (source, power) => {
    let url = new URL(host + '/' + source);
    let params = { powerStatus: power };
    url.search = new URLSearchParams(params).toString();
    try {
        const response = await fetch(url);
        return await response.json();
    }
    catch (err){
        console.log(err);
        return null;
    }
}

const updateState = (state) => {
    console.log(state);
}

window.addEventListener("load", init);
//Event Stream
var source = new EventSource(host + '/stream');
window.addEventListener("message", (event) => {
    state = event.data;
    update_state(state);
});
