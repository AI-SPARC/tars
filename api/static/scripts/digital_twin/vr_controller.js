scene = document.getElementById("scene");

function onTriggerDown(e){
  if (currentElement != undefined){
    switch (currentElement.id){
      case "jointModeButton":
        if(state != 0){ 
          state = 0
          changeText(stateText, `Current Mode[Joint Control]`);
          updateHUD(state)
        }
        break;

      case "toolModeButton":
        if(state != 1){
          state = 1
          changeText(stateText, `Current Mode[Tool Control]`);
          updateHUD(state)
        }
        break;

      case "increase_j0":
        if(state == 0){
          jointsPosition[0] += 10
          const new_positions = jointsPosition.map(function(element) {return element.toFixed(1);}).join(" ");
          client.publish('denso/target_positions', new_positions);
        }
        else if(state == 1){
          calculateNewPositions()
          client.publish('denso/target_positions', `${new_position}`);
        }
        break;

      case "decrease_j0":
        if(state == 0){
          jointsPosition[0] -= 10
          const new_positions = jointsPosition.map(function(element) {return element.toFixed(1);}).join(" ");
          client.publish('denso/target_positions', new_positions);
        }
        else if(state == 1){
          calculateNewPositions()
          client.publish('denso/target_positions', `${new_position}`);
        }
        break;

    }
  }
}