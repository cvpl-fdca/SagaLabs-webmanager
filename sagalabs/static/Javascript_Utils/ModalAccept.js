class ModalAccept{

    // DEPENDENCIES:
    // BOOTSTRAP 5 JS BUNDLE: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js
    // BOOTSTRAP 5 CSS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css

    constructor(modalHTML){
        this.modalHTML = modalHTML;
        this.modalBootstrap = new bootstrap.Modal(modalHTML)
        this.acceptButton = modalHTML.querySelector('.btn-primary');
        this.currentEventListeners = false;
    }

    display(title, text, onAccept, onClose = () => null){
        let closeWithoutEvent = false

        const onAcceptWrapper = () => {
            closeWithoutEvent = true
            this.modalBootstrap.hide()
            onAccept()
        }

        const onCloseWrapper = () => {
            if(!closeWithoutEvent){
                onClose()
            }
        }

        //Remove old event listeners
        if(this.currentEventListeners){
            this.acceptButton.removeEventListener('click', this.currentEventListeners[0]);
            this.modalHTML.removeEventListener('hidden.bs.modal', this.currentEventListeners[1])
        }
        //Set title and body
        this.modalHTML.querySelector('.modal-title').innerHTML = title;
        this.modalHTML.querySelector('.modal-body').innerHTML = text;
        //Set new event listeners
        this.acceptButton.addEventListener('click', onAcceptWrapper);
        this.modalHTML.addEventListener('hidden.bs.modal', onCloseWrapper);
        this.currentEventListeners = [onAcceptWrapper, onCloseWrapper]
        //Activate modal
        this.modalBootstrap.show()
    }
}