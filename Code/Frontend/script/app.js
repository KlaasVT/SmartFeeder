const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const clearClassList = function (el) {
  el.classList.remove("c-room--wait");
  el.classList.remove("c-room--on");
};

const listenToUI = function () {
  
  // const knoppen = document.querySelectorAll(".js-humidity-btn");
  // for (const knop of knoppen) {
  //   knop.addEventListener("click", function () {
      
  //     const id = this.dataset.idlamp;
  //     let nieuweStatus;
  //     if (this.dataset.statuslamp == 0) {
  //       nieuweStatus = 1;
  //     } else {
  //       nieuweStatus = 0;
  //     }
  //     //const statusOmgekeerd = !status;
  //     clearClassList(document.querySelector(`.js-room[data-idlamp="${id}"]`));
  //     document.querySelector(`.js-room[data-idlamp="${id}"]`).classList.add("c-room--wait");
      
  //     socket.emit("F2B_inlezen_sensor");
  //   });
  // }

  const knoppen = document.querySelectorAll(".js-btn");
  for(const knop of knoppen){
    knop.addEventListener("click",function(){
      const id = this.dataset.id;
      const type = this.dataset.type;
      if(type == "A"){
        socket.emit("F2B_aansturen_actuator",{actuator: id})
      }else if(type == "S"){
        socket.emit("F2B_inlezen_sensor",{sensor: id})
      }

    })
  }
};

const listenToSocket = function () {
  socket.on("connected", function () {
    console.log("verbonden met socket webserver");
  });

  //in stap 2
  
  socket.on("B2F_inlezing_sensor",function(jsonObject){
    console.log("Er is een inlezing van sensoren gebeurt");
    console.log(jsonObject)
    const button = document.querySelector(".js-btn");
    button.innerHTML = jsonObject.waarde[0].Value;
  });
};

document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
  listenToUI();
  listenToSocket();
});
