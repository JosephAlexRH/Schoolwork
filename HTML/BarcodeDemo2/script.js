
window.onload = function () {
  const videoContainer = document.getElementById("video");
  const resultText = document.getElementById("result");
  function order_by_occurence(arr) {
    var counts = {};
    arr.forEach(function (i) {
      if(!counts[i]){
        counts[i] = 0;
      }
      counts[i]++;
    });
    return Object.keys(counts).sort(function (a, b) {
      return counts[b] < counts[a];
    });
  }

  Quagga.init(
    {
      inputStream: {
        name: "Live",
        type: "LiveStream",
        numOfWorkers: navigator.hardwareConcurrency,
        target: videoContainer
      },
      decoder: {
        readers: ["ean_reader"]
      }
    },
    function (err) {
      if (err) {
        console.log(err);
        return;
      }

      Quagga.start();
    });

  var last_result=[];
  Quagga.onDetected(function (result) {
    var last_code = result.codeResult.code;
    last_result.push(last_code);

    if(last_result.length>20){
      code=order_by_occurence(last_result)[0];
      last_result=[];
      Quagga.stop();
      alert("Detected barcode: " + last_code);
    }
  });
};
