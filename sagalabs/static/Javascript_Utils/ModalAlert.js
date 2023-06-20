class ModalAlert{

    // DEPENDENCIES:
    // BOOTSTRAP 5 JS BUNDLE: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js
    // BOOTSTRAP 5 CSS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css

    constructor(modalHTML){
        this.modalHTML = modalHTML;
        this.modalBootstrap = new bootstrap.Modal(modalHTML)
        this.currentEventListener = false;
    }

    display(title, text, onClose = () => null){

        //Remove old event listeners
        if(this.currentEventListener){
            this.modalHTML.removeEventListener('hidden.bs.modal', this.currentEventListener)
        }
        //Set title and body
        this.modalHTML.querySelector('.modal-title').innerHTML =  "<b>" + title + "/<b>";
        this.modalHTML.querySelector('.modal-body').innerHTML = text;
        //Set new event listeners
        this.modalHTML.addEventListener('hidden.bs.modal', onClose);
        this.currentEventListeners = onClose
        //Activate modal
        this.modalBootstrap.show()
    }
}