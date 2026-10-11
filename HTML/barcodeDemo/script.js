window.onload = function() {
    const videoContainer = document.getElementById("video");
    const resultText = document.getElementById("result");

    Quagga.init(
        {
            inputStream: {
                type: "LiveStream",
                constraints: {
                    width: 480,
                    height: 320,
                    facingMode: "environment"
                },
                target: videoContainer
            },
            decoder: {
                readers: ["ean_reader", "ean_13_reader"]
            }
        },
        (err) => {
            if (err) {
                console.error("Quagga initialization failed:", err);
                return;
            }
            Quagga.start();
        }
    );

    Quagga.onDetected((data) => {
        let barcode = data.codeResult.code;
        resultText.innerText = `Scanned: ${barcode}`;

        Quagga.stop();
        fetchProductInfo(barcode);
    });

    function fetchProductInfo(barcode) {
        fetch(`https://world.openfoodfacts.org/api/v0/product/${barcode}.json`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 1) {
                    let product = data.product;
                    let message = `📦 Product: ${product.product_name || "Unknown"}\n🏷️ Brand: ${product.brands || "Unknown"}\n📂 Category: ${product.categories || "Unknown"}`;

                    alert(message);
                    if (product.image_url) window.open(product.image_url, "_blank");
                } else {
                    alert("❌ Product not found.");
                }
            })
            .catch(error => {
                console.error("Error fetching product info:", error);
                alert("⚠️ Error fetching product details.");
            });
    }
};
