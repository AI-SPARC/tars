const url = "mqtt://127.0.0.1:9001"

const client = mqtt.connect(url);

const topics = [
  "kukaYoubot/v2/ic/001",
  "kukaYoubot/v2/ic/002",
  "kukaOmnirob/v2/ic/001"
]

client.on('connect', function () { 
  console.log("Connected to MQTT broker")

  topics.map(
    (topic) => 
    client.subscribe(`${topic}`, (err) => {
      if (!err) {
        console.log(`Subscribed to: ${topic}`)
      }
      else{
        console.log(`Error subscribing to: ${topic}`)
      }
    }));
  }
)

client.on('message', function (topic, message) {
  // console.log(topic, message)
  const stringMsg = message.toString();
  const arrayMsg = stringMsg.split(',').map(Number);

  const fomartedArrayMsg = arrayMsg.map(num => {
    // Limitar rotação no if
    if (!isNaN(num)) {
      return (parseFloat(num) * 180/Math.PI).toFixed(2);
    } else {
      return num;
    }
  });
  jointsPosition = fomartedArrayMsg
  updateJoints(fomartedArrayMsg)
  updateHUD(state)
})