customElements.define(
  "file-size",
  class extends HTMLElement {
    connectedCallback(
      // BYTE SAVINGS: DECLARE variables/functions as parameters to prevent 4 bytes let statement
      // source file to get content-length of:
      source = this.getAttribute("src") ||
        "https://file-size.github.io/element.js",
      // global state to load gzthermal IMG once
      img = false,
      // display bigger than maxbytes in red color
      maxbytes = this.getAttribute("max") || 49152, // 48 kByte, because my first TRS-80 had 48 kB RAM
      // load GZThermal IMG function:
      gzthermal = () => {
        if (!img) {
          this.querySelector("i").innerHTML = "Loading GZIP Thermal analysis";
          img = this.querySelector("img");
          img.onerror = (e) =>
            (this.querySelector("i").innerHTML = "Too many bytes for analysis");
          img.onload = (e) => {
            this.querySelector("i").innerHTML = "";
            img.style.width = (this.getAttribute("width") || "700") + "px";
            this.querySelector("details").setAttribute("open", "open");
            img.onclick = (e) => {
              if (e.altKey) open(source, "_blank").focus(); // open new tab with source code
              else this.querySelector("details").removeAttribute("open");
            };
          };
          img.src = "https://gzthermal.vercel.app/?url=" + source;
        }
      }
    ) {
      this.setAttribute("title", source);
      fetch(source, {
        mode: "cors",
      })
        .then((response) => {
          this.length = Number(response.headers.get("content-length"));

          this.innerHTML =
            `<details style="cursor:pointer;font:16px arial">` +
            `<summary>` +
            `<b style="color:dark${
              this.length < maxbytes ? "green" : "red"
            };display:inline-block;width:4em;text-align:right">${
              this.length
            }</b> &nbsp;Bytes ${source} <i/>` +
            `</summary><img/>` +
            `</details>`;

          // toggle display GZThermal IMG
          this.querySelector("details").ontoggle = (e) => {
            this.querySelector("details").open && gzthermal();
          };

          if (this.hasAttribute("gz")) gzthermal(); // load GZThermal IMG by default
        })
        .catch((e) => {
          this.innerHTML = `<b style="font:16px arial;color:red">&lt;file-size> ${e} : ${source}</b>`;
        });
    }
  }
);
