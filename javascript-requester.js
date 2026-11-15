function Get()
{
  console.log("fetching");
  let f = fetch("http://188.220.221.17:8080");
  console.log(f);
}
async function Get2() {
  console.log("fetching...");
  try {
    let response = await fetch("http://188.220.221.17:8080");
    
    // Check if the request was successful
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    let text = await response.text();
    console.log("Response data:", text);
  } catch (error) {
    console.error("Fetch failed:", error);
  }
}
async function GetFromURL(url = "https://img.magnific.com/free-photo/closeup-shot-beautiful-butterfly-orange-petaled-flower_181624-13884.jpg?semt=ais_hybrid&w=740&q=80") {
  console.log("fetching...");
  try {
    let response = await fetch("http://188.220.221.17:8080", {
      method: "POST", // Specify the method (POST, PUT, etc.)
      headers: {
        "Content-Type": "text/plain" // Tell the server you are sending plain text
      },
      body: url // The text you want to send
    });
    
    // Check if the request was successful
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Expect and read the response from the server
    let text = await response.text();
    console.log("Response data:", text);
  } catch (error) {
    console.error("Fetch failed:", error);
  }
}