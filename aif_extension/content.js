// @ts-check

const checkedImages = new WeakSet()

async function CheckImageForAI(imgUrl) {
    await new Promise((resolve) => setTimeout(resolve,200));

    return {
        isAI : true
    }
}

function VisuallyFlagImage(img) {
    const parent = img.parentElement;
    if (!parent) return;
    console.log("1")
    if (getComputedStyle(parent).position === "static") {
        parent.style.position = "relative";
    }
    console.log("2")
    const badge = document.createElement("div");
    badge.textContent = `LIKELY AI GENERATED`;
    console.log("3")
    Object.assign(badge.style, {
        position: "absolute",
        top: "8px",
        left: "8px",
        backgroundColor: "rgba(220, 38, 38, 0.9)",
        color: "white",
        padding: "4px 8px",
        borderRadius: "4px",
        fontSize: "12px",
        fontWeight: "bold",
        fontFamily: "sans-serif",
        zIndex: "9999",
        pointerEvents: "none"
    });
    console.log("flagged successfully");

    img.style.outline = "2px solid #000000";
    parent.appendChild(badge);
}

function FlagSafe(img) {
    const parent = img.parentElement;
    if (!parent) return;
    console.log("1")
    if (getComputedStyle(parent).position === "static") {
        parent.style.position = "relative";
    }
    console.log("2")
    const badge = document.createElement("div");
    badge.textContent = `REAL`;
    console.log("3")
    Object.assign(badge.style, {
        position: "absolute",
        top: "8px",
        left: "8px",
        backgroundColor: "rgba(220, 38, 38, 0.9)",
        color: "white",
        padding: "4px 8px",
        borderRadius: "4px",
        fontSize: "12px",
        fontWeight: "bold",
        fontFamily: "sans-serif",
        zIndex: "9999",
        pointerEvents: "none"
    });
    console.log("flagged successfully");

    img.style.outline = "2px solid #000000";
    parent.appendChild(badge);
}

async function GetFromURL(url = "https://img.magnific.com/free-photo/closeup-shot-beautiful-butterfly-orange-petaled-flower_181624-13884.jpg?semt=ais_hybrid&w=740&q=80") {
  console.log("fetching...");
  try {
    console.log("checking url")
    let response = await fetch("https://188.220.221.17:8080", {
      method: "POST", // Specify the method (POST, PUT, etc.)
      headers: {
        "Content-Type": "text/plain" // Tell the server you are sending plain text
      },
      body: url // The text you want to send
    });
    console.log(response);
    // Check if the request was successful
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Expect and read the response from the server
    let text = await response.text();
    console.log(text);
    if (text == "REAL") {
        return false
    } 
    else {
        return true
    }

  } catch (error) {
    console.error("Fetch failed:", error);
  }
}

async function ScanImage(img) {
    if (checkedImages.has(img)) return;
    checkedImages.add(img);

    //to stop it checking loads of tiny images and icons and shite
    if (img.naturalWidth < 100 || img.naturalLength < 100) return;
    if (!img.src) return;
    //if (img.src.startsWith("data:")) return;
    const result = await GetFromURL(img.src);
    let fake = result?.valueOf()
    console.log("FAKE: "+ fake);
    if (fake) {
        console.log("flagging");
        VisuallyFlagImage(img)
    }
    else
    {
        console.log("flagging safe");
        FlagSafe(img);
    }
}

document.querySelectorAll("img").forEach((img) => {
    if (img.complete) {
        ScanImage(img);
    }   else {
        img.addEventListener("load", () => ScanImage(img))
    }
});

function handleImageElement(img) {
  if (img.complete && img.naturalWidth > 0) {
    processImage(img);
  } else {
    img.addEventListener("load", () => processImage(img), { once: true });
  }
}

const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
            if (node.tagName === "IMG") {
                node.addEventListener("load", () => ScanImage(node));
            }   else if (node.querySelectorAll) {
                node.querySelectorAll("img").forEach((img) => {
                    img.addEventListener("load", () => ScanImage(img));
                });
            }
        });
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});