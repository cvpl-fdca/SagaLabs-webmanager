class ModalAccept{

    // DEPENDENCIES:
    // BOOTSTRAP 5 JS BUNDLE: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js
    // BOOTSTRAP 5 CSS: https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css

    constructor(modalHTML){
        this.modalHTML = modalHTML;
        this.modalBootstrap = new bootstrap.Modal(modalHTML)
        this.acceptButton = modalHTML.querySelector('.btn-primary');
        this.declineButton = modalHTML.querySelector('.btn-secondary');
        this.currentEventListeners = false;
    }

    // title and text is of type string
    // onAccept is a fucntion without arguments but may return a promise - onAccept is called uppon user clicking 'Yes'.
    // onClose is an optional and is a function without arguments - onClose is called uppon user closing the modal in any way.
    // This method is used to display the modal and should only be called once.
    display(title, text, onAccept = () => null, onClose = () => null){
        let closeWithoutEvent = false

        const onAcceptWrapper = () => {
            const closeModal = () => {
                this.modalBootstrap.hide()
            }
            closeWithoutEvent = true
            const resultFromAccept = onAccept()
            //Check if result of calling onAccept is a Promise
            if(resultFromAccept instanceof Promise){
                //Show spinning wheel and wait for fulfilled before closing
                this.declineButton.disabled = true;
                this.acceptButton.disabled = true;
                this.acceptButton.innerHTML = '<span class="spinner-border spinner-border-sm mx-1" role="status" aria-hidden="true"></span>';
                resultFromAccept.then(() => {
                    closeModal()
                })
            } else {
                closeModal()
            }

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
        this.modalHTML.querySelector('.modal-title').innerHTML = "<b>" + title + "</b>";
        this.modalHTML.querySelector('.modal-body').innerHTML = text;
        //Set new event listeners
        this.acceptButton.addEventListener('click', onAcceptWrapper);
        this.modalHTML.addEventListener('hidden.bs.modal', onCloseWrapper);
        this.currentEventListeners = [onAcceptWrapper, onCloseWrapper]
        //Activate modal
        this.modalBootstrap.show()
    }
}