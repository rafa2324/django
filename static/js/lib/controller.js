/*
Development by Edgard Ramos  ismytv@gmail.com
*/
class Controller {
    constructor(url, data, function_response) {
        this.url = url;
        this.data = data;
        this.function_response = function_response;
        // Cada formulario debe tener la declaracion del tag: 
        // (ESTO ES EN FLASK)
        //  <meta name="csrf-token" content="{{ csrf_token() }}"></meta>
        // this.csrf_token = document.querySelector('meta[name="csrf-token"]').content;
        this.csrf_token = getCookie('csrftoken');
    }

    async fetch_action() {
        // Ejecuta la llamada fetch y luego de recibir respuesta llamará a la funcion definida por 
        // el usuario en this.function_response enviando como parámetro: response.status y la data 
        // recibida (diccionario)
        // No errors
        try {
            const response = await fetch(`${window.origin}${this.url}`, {
                method: "POST",
                credentials: "include",
                body: JSON.stringify(this.data),
                cache: "no-cache",
                headers: new Headers({
                    "content-type": "application/json",
                    'X-CSRFToken': this.csrf_token
                })
            });
            if (!response.ok) 
                throw new Error(`HTTP error! status: ${response.status}`);
            else {
                let data = await response.json();
                this.function_response(response.status, data);
            }
        } catch(e) {
            console.log(`Fetch error: ${e}`);
        }
    }
}