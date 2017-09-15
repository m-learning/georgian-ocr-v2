(function () {
	function createInput (id) {
		var input = document.createElement('input')
		
		input.type = 'text'
		input.style.width = '64px'
		input.style.height = '64px'
		input.style.margin = '0px'
		input.style.position = 'absolute'
		input.style.bottom = '1px'
		input.style.left = '1px'
		input.style.fontSize = '20px'
		input.style.fontWeight = 'bold'
		input.style.textAlign = 'center'
		input.style.border = DEFAULT_BORDER
		
		input.addEventListener('focus', function (e) {
			e.target.blur()
			selectInput(e.target)
		})
		input.id = 'input' + id
		return input
	}
	
	function createImage (id, src) {
		var img = new Image()
		
		img.style.width = '64px'
		img.style.height = '64px'
		img.style.margin = '0px'
		img.style.position = 'absolute'
		img.style.top = '1px'
		img.style.left = '1px'
		img.style.display = 'inline-block'
		img.style.border = DEFAULT_BORDER
		img.src = src
		
		return img
	}
	
	function createCell (id, imageSrc) {
		var div = document.createElement('div')
		div.style.position = 'relative'
		div.style.width = '66px'
		div.style.height = '140px'
		div.style.padding = '1px'
		div.style.margin = '0px'
		div.style.display = 'inline-block'
		
		var image = createImage(id, imageSrc)
		var input = createInput(id)
		
		div.appendChild(image)
		div.appendChild(input)
		
		div.image = image
		div.input = input
		
		return div
	}
	
	var keyCodes = {
		65: 'ა',
		66: 'ბ',
		71: 'გ',
		68: 'დ',
		69: 'ე',
		86: 'ვ',
		90: 'ზ',
		73: 'ი',
		75: 'კ',
		76: 'ლ',
		77: 'მ',
		78: 'ნ',
		79: 'ო',
		80: 'პ',
		82: 'რ',
		83: 'ს',
		84: 'ტ',
		85: 'უ',
		70: 'ფ',
		81: 'ქ',
		89: 'ყ',
		67: 'ც',
		87: 'წ',
		88: 'ხ',
		74: 'ჯ',
		72: 'ჰ'
	}
	
	var shiftedKeyCodes = {
		84: 'თ',
		74: 'ჟ',
		82: 'ღ',
		83: 'შ',
		67: 'ჩ',
		90: 'ძ',
		87: 'ჭ'
	}
	
	var otherSymbols = ['=', '-', ',', ';', ':', '!', '?', '.',
						'\'', '"', '(', ')', '*', '%', '+',
						'0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	
	var DEFAULT_BORDER = '0.1px solid grey'
	var SELECTED_BORDER = '2px solid green'
	var COMPLETED_COLOR = 'rgba(142, 230, 142, 0.2)'
	var SELECTED_COLOR = 'rgba(142, 230, 142, 0.4)'
	var DISABLED_COLOR = 'rgba(230, 142, 142, 0.3)'
	var EMPTY_COLOR = '#fff'
	
	var aEN = 65
	var aGE = 4304
	var specialKeys = ['Shift']
	
	var containerDiv = document.getElementById('container')
	
	var selectedInput
	var finished = false
	
	document.addEventListener('keydown', keyHandler, false)
	
	document.getElementById('new-button').addEventListener('click', function () {
		location.href = "/"
	})
	
	var saveButton = document.getElementById('save-button')
	saveButton.disabled = 'disabled'
	saveButton.addEventListener('click', function () {
		var canvas = document.createElement('canvas')
		var c = canvas.getContext('2d')
		
		var data = []
		
		for (var i = 0; i < containerDiv.children.length; i++) {
			var img = containerDiv.children[i].image
			var input = containerDiv.children[i].input
			if (input.disabled) continue
			
			canvas.width = img.naturalWidth	
			canvas.height = img.naturalHeight
			c.clearRect(0, 0, canvas.width,canvas.height)
			c.drawImage(img, 0, 0)
			data.push({
				image: canvas.toDataURL().substring(22),
				result: input.value
			})
		}
		
		var formData = new FormData
		formData.append('data', JSON.stringify(data))
		
		var oReq = new XMLHttpRequest();
		oReq.addEventListener("load", function () {
			if (this.responseText == 'OK') {
				init()
				showMessage('მონაცემები შენახულია')
			}
		})
		oReq.open("POST", "save")
		oReq.send(formData)
	})
	
	init()
	
	function init () {
		containerDiv.innerHTML = ''
		
		var oReq = new XMLHttpRequest();
		oReq.addEventListener("load", function () {
			var data
			try {
				data = JSON.parse(this.responseText)
			} catch (ex) {}
			
			if (data) {
				for (var i = 0; i < data.length; i++) {
					containerDiv.appendChild(createCell(i, data[i]))
				}
				
				selectFirstInput()
			}
		})
		oReq.open("GET", "load")
		oReq.send()
	}
	
	function selectFirstInput () {
		selectInput(containerDiv.children[0].input)
	}
	
	function selectInput (input) {
		if (!input) return
		
		if (selectedInput) {
			selectedInput.style.border = DEFAULT_BORDER
			if (selectedInput.value) {
				selectedInput.style.backgroundColor = COMPLETED_COLOR
			} else {
				if (selectedInput.disabled) {
					selectedInput.style.backgroundColor = DISABLED_COLOR
				} else {
					selectedInput.style.backgroundColor = EMPTY_COLOR
				}
			}
		}
		
		input.style.border = SELECTED_BORDER
		input.style.backgroundColor = SELECTED_COLOR
		
		selectedInput = input
	}
	
	function selectNextInput () {
		var index = getInputIndex(selectedInput)
		if (index != -1) {
			if (index < containerDiv.children.length - 1) {
				selectInput(containerDiv.children[index + 1].input)
			}
		}
	}
	
	function selectPreviousInput () {
		var index = getInputIndex(selectedInput)
		if (index != -1) {
			if (index > 0) {
				selectInput(containerDiv.children[index - 1].input)
			}
		}
	}
	
	function getInputIndex (el) {
		for (var i = 0; i < containerDiv.children.length; i++) {
			if (containerDiv.children[i].input == el) {
				return i;
			}
		}
		
		return -1
	}
	
	function disableSelectedInput () {
		if (selectedInput) {
			selectedInput.disabled = 'disabled'
			selectedInput.style.backgroundColor = DISABLED_COLOR
			selectedInput.parentNode.children[0].style.opacity = 0.8
			selectedInput.value = ''
			selectNextInput()
		}
	}
	
	function enableSelectedInput () {
		if (selectedInput) {
			selectedInput.disabled = ''
			if (!selectedInput.value) {
				selectedInput.style.backgroundColor = EMPTY_COLOR
			}
			selectedInput.parentNode.children[0].style.opacity = 1
		}
	}
	
	
	var timeout
	function keyHandler (e) {
		var value
		
		if (e.key === 'ArrowLeft') {
			clearTimeout(timeout)
			selectPreviousInput()
		} else if (e.key === 'ArrowRight') {
			clearTimeout(timeout)
			selectNextInput()
		} else if (e.key === 'ArrowDown') {
			clearTimeout(timeout)
			disableSelectedInput()
		} else if (e.key === 'ArrowUp') {
			clearTimeout(timeout)
			enableSelectedInput()
		} if (e.key === 'Backspace') {
			clearTimeout(timeout)
			selectPreviousInput()
			selectedInput.value = ''
		} if (e.key === 'Delete') {
			clearTimeout(timeout)
			selectNextInput()
			selectedInput.value = ''
		} else if (specialKeys.indexOf(e.key) === -1) {
			if (e.shiftKey) {
				value = shiftedKeyCodes[e.keyCode]
			} else {
				value = keyCodes[e.keyCode]
			}
			
			if (!value && otherSymbols.indexOf(e.key) != -1) {
				value = e.key
			}
			
			clearTimeout(timeout)
		
			if (value && selectedInput && !finished) {
				selectedInput.value += value
				enableSelectedInput()
				
				timeout = (function (input) {
					return setTimeout(function () {
						selectInput(input)
					}, 1000)
				})(selectedInput)
				
				selectNextInput()
			}
		}
		
		if (checkFinished()) {
			finished = true
			saveButton.disabled = ''
		} else {
			finished = false
			saveButton.disabled = 'disabled'
		}
	}
	
	function checkFinished () {
		if (!containerDiv.children.length) return false
		
		for (var i = 0; i < containerDiv.children.length; i++) {
			var input = containerDiv.children[i].input
			if (!input.disabled && !input.value) {
				return false
			}
		}
		
		return true
	}
	
	function showMessage (msg) {
		var div = document.getElementById('message-div')
		
		div.innerHTML = msg
		
		div.style.display = 'block'
		
		setTimeout(function () {
			div.style.display = 'none'
		}, 3000)
	}
})()
