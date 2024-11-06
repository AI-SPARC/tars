AFRAME.registerComponent("clicable", {
  init: function () {
    let el = this.el;

    this.onRaycastHit = (evt) => {
      currentElement = el;
    };

    this.onRaycastClear = (evt) => {
      currentElement = undefined;
    };

    this.el.addEventListener("raycaster-intersected", this.onRaycastHit);
    this.el.addEventListener(
      "raycaster-intersected-cleared",
      this.onRaycastClear
    );
  },

  remove: function () {
    this.el.removeEventListener("raycaster-intersected", this.onRaycastHit);
    this.el.removeEventListener(
      "raycaster-intersected-cleared",
      this.onRaycastClear
    );
  },
});

AFRAME.registerComponent('thumbstick-logging-right',{
  init: function () {
    this.el.addEventListener('thumbstickmoved', this.logThumbstick);
  },
  
  logThumbstick: function (evt) {
      let deltaTheta = evt.detail.x/20.0;
      player.rotation.y -= deltaTheta;
    }
  });

AFRAME.registerComponent('controller_events',{
  init: function () {
    this.el.addEventListener("triggerdown", onTriggerDown);
  }
});