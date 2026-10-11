function load_quagga (){
  if($('barcode-scanner').length > 0 && navigator.mediaDevices.getUserMedia && typeof navigator.mediaDevices.getUserMedia === 'function') {
    Quagga.init({},{
      inputStream: {
        name: "Live",
        type: "LiveStream",
        numOfWorkers: navigator.hardwareConcurrency,
        target: document.querySelector('#barcode-scanner'),
      },
      decoder: {
        readers: ['ean_reader', 'ean_8_reader', 'code_39_reader', 'code_39_vin_reader', 'codabar_reader', 'upc_reader', 'upc_e_reader']
      }
    },function(err){
      if(err){
        console.log(err);
        return;
      }
      Quagga.start();
    })
  }
};
