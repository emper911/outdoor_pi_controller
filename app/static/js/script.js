// const host = "http://OutdoorController:3000/garden";
const host = "http://192.168.1.205:80/garden";

let state = {
    power: {
        lights: false,
        pump: false,
        misc: false,
    }
}

const init = async () => {
    //initalize state
    await initState();
    //get button elements
    await initButtons();
    //Event Stream
    initEventStreamHandler();

}

const initState = async () => {
    let url = new URL(host + '/' + 'state');
    try {
        const response = await fetch(url, {
    		method: 'GET', // *GET, POST, PUT, DELETE, etc.
    		mode: 'no-cors', // no-cors, *cors, same-origin );
	});
        state = await response.json();
        console.log(`Starting State: ${JSON.stringify(state)}`);
    } catch (err) {
        console.log(err);
        return null;
    } 
};

const initButtons = async () => {
    // Get a list of button elements by source
    let powerButtons = Object.keys(state.power).map((source) => {
        return document.getElementById(`${source}`)
    });
    // Attach power button handler and updates active buttons
    powerButtons.map((button) => {
        button.addEventListener("click", powerButtonHandler);
        (state.power[button.id]) ?
            button.classList.add("controller-buttons-active")
        :
            button.classList.remove("controller-buttons-active")
    });
}

const initEventStreamHandler = () => {
    const source = new EventSource(host + '/stream');
    source.addEventListener('open', () => console.log("Sse connection opened"));
    source.addEventListener('error', () => console.log("error occured"));
    
    source.addEventListener("message", (event) => {
        responseJson = JSON.parse(event.data);
        updateState(responseJson);
    });
};

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
}

/*
######################################################################
########################## Helper Functions ##########################
######################################################################
*/
const updateState = async (newState) => {
    state = newState;
    await updateButtons();
}

const updateButtons = async () => {
    let powerButtons = Object.keys(state.power).map((source) => {
        return document.getElementById(`${source}`)
    });
    //attach event listeners and update active buttons
    powerButtons.map((button) => {
        (state.power[button.id]) ?
            button.classList.add("controller-buttons-active")
            :
            button.classList.remove("controller-buttons-active")
    });
}

const relaySwitch = async (source, power) => {
    let url = new URL(host + '/' + source);
    let params = { powerStatus: power };
    url.search = new URLSearchParams(params).toString();
    try {
        const response = await fetch(url, {
	    method: 'GET', // *GET, POST, PUT, DELETE, etc.
	    mode: 'no-cors', // no-cors, *cors, same-origin);
	});
        return await response.json();
    } catch (err){
        console.log(err);
        return null;
    }
}


window.addEventListener("load", init);
