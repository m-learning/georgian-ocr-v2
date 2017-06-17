upload = function(el){
  document.getElementById('loading').style.display="block"
  document.getElementById('result').innerHTML = ''
  var file = el.files[0]
  var fd = new FormData();
  fd.append("file", file);
  var url = '../upload'
  var xhr = new XMLHttpRequest()
  xhr.open('POST', url, true)
  xhr.onload = function() {
    if (this.status == 200) {
      document.getElementById('result').innerHTML=this.response
    }

    var newInput = document.createElement("input"); 

    newInput.type = "file"; 
    newInput.id = el.id; 
    newInput.name = el.name; 
    newInput.className = el.className; 
    newInput.style.cssText = el.style.cssText; 
    newInput.addEventListener('change', function(){upload(newInput)})
    newInput.accept = 'image/*'
    el.parentNode.replaceChild(newInput, el); 
    document.getElementById('loading').style.display="none"
  }
  xhr.send(fd)
}
