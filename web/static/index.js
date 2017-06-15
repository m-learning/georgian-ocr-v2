upload = function(el){
  var file = el.files[0]
  var fd = new FormData();
  fd.append("file", file);
  var url = '../upload'
  var xhr = new XMLHttpRequest()
  xhr.open('POST', url, true)
  xhr.onload = function() {
    if (this.status == 200) {
      console.log(this)
      document.getElementById('result').innerHTML=this.response
    }
  }
  xhr.send(fd)
}
