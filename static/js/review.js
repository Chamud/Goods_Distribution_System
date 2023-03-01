const style = document.createElement('template');
style.innerHTML = `

<style type="text/css">
.rating{
  display : flex;
  height  : 48px;
}

.rating input{
  position : absolute;
  left     : -150vw;
}

.rating label{
  width      : 48px;
  height     : 48px;
  padding    : 0;
  overflow   : hidden;
  background : url('https://iamkate.com/code/star-rating-widget/stars.svg') no-repeat top left;
}

.rating:not(:hover) input:indeterminate + label,
.rating:not(:hover) input:checked ~ input + label,
.rating input:hover ~ input + label{
  background-position : -48px 0;
}

.rating:not(:hover) input:focus-visible + label{
  background-position : -96px 0;
}
</style>
`

class Review extends HTMLElement{
	constructor(){
		super();
		this.attachShadow({ mode: 'open'});
     	this.shadowRoot.appendChild(style.content.cloneNode(true));	
     }

	connectedCallback(){

		var val    = this.hasAttribute('value') ? this.getAttribute('value') : 0;


		const cont    = document.createElement('div');
		const shadow = this;

		for (var i = 1; i <= 5; i++) {
	  		const inp    = document.createElement('input');
	  		const lbl    = document.createElement('label');

	  		cont.setAttribute('class','rating');
	  		inp.setAttribute('type','radio');
	  		inp.setAttribute('name','rating');  		
  			inp.setAttribute('id','rating'+i);
  			inp.setAttribute('value', i);
  			lbl.setAttribute('for','rating'+i);

  			inp.onclick = function() {
		            shadow.setAttribute("value", this.value);
		        }

		       if(i==val) inp.checked = true;

  			cont.appendChild(inp);
  			cont.appendChild(lbl);
  		}
		this.shadowRoot.appendChild(cont);
 	}

 	static get observedAttributes(){
	}

 	attributeChangedCallback(name, oldValue, newValue){
		
	}
}

window.customElements.define('five-stars', Review);

