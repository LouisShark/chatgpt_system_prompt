customElements.define("fit-text", class extends HTMLElement {
    constructor() {
        super()
            .attachShadow({ mode: "open" })
            .innerHTML = `<slot style=display:inline-block>` +
            `<style>:host{display:inline-block;width:100%;white-space:nowrap`
    }
    connectedCallback(// define variables and functions as parameters to save LET declarations
        slot = this.shadowRoot.querySelector("slot"),
        // FUNCTION fit text to fit the <fit-text> element
        fit = _ =>
            setTimeout(
                _ => this.style.fontSize = parseInt(getComputedStyle(slot).fontSize) * (this.clientWidth / slot.scrollWidth) + "px"
            ),
        // FUNCTION add listener; return removeEventListener function
        event = (root, name, x = root.addEventListener(name, fit)) => x => root.removeEventListener(name, fit),
        observers = [] //array of MutationObservers
    ) {
        fit() // fit the text on first load

        // watch for any (any!) DOM changes, unless the "static" attribute is set
        if (!this.hasAttribute("static")) {
            // Listeners outside 'this' need to be removed on disconnect! Keep a reference
            this.r = event(window, "resize") // fit when the window resizes
            this.l = event(document.fonts, "loadingdone") // fit when fonts load

            slot.addEventListener("slotchange", (e) => {
                // watch new Child elements with shadowRoots, attach MutationObserver
                [...slot.assignedElements()]
                    .filter(x => x.shadowRoot && !x.observer)
                    .map(x => {
                        observers.push(x.observer = new MutationObserver(fit))
                        x.observer.observe(x.shadowRoot, { childList: true, subtree: true, characterData: true })
                    })
            })
            // MutationObserver for all <fit-text> lightDOM changes
            observers.push(this.observer = new MutationObserver(fit))
            this.observer.observe(this, { childList: true, subtree: true, characterData: true })
        }
    }
    disconnectedCallback() {
        this.r() // remove "resize" listener
        this.l() // remove font "loadingdone" listener
        observers.map(x => x.disconnect()) // remove all MutationObservers
    }
});