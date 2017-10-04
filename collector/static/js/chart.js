(function () {
	var timeout;
	var canvas = document.createElement('canvas')
	canvas.width = 1050
	canvas.height = 400
	canvas.className = 'chart'
	
	var chartW = 950
	var chartH = 330
	
	var left = 80
	var bottom = 360
	
	var c = canvas.getContext('2d')
    c.font = "14px monospace"
	
	document.body.appendChild(canvas)
	
    function loadChartData () {
		var oReq = new XMLHttpRequest()
		oReq.addEventListener('load', function () {
			var data
			try {
				data = JSON.parse(this.responseText)
			} catch (ex) { }
			
			data.sort((a, b) => {
			    return a.label > b.label ? 1 : -1;
		    })
			
		    drawChart(data)
		})
		
		oReq.open('GET', 'chartData')
		oReq.send()
    }
    
    loadChartData()
    
    function findMaxCount (data) {
        var m = 0;
        data.forEach(d => {
            m = Math.max(m, d.count)
        })
        return m;
    }
    
    function drawBackground () {
        c.save()
        c.fillStyle = '#f0f0f0'
        c.fillRect(0, 0, canvas.width, canvas.height)
        c.restore()
    }
    
    function drawX () {
    
        c.beginPath()
        c.moveTo(left - 20, bottom)
        c.lineTo(left + chartW, bottom)
        c.stroke()
    }
    
    function drawY () {
        
        c.moveTo(left, bottom + 20)
        c.lineTo(left, bottom - chartH)
        c.stroke()
    }
    
    function drawXLabels (data, maxCount) {
        c.save()
        c.textAlign = 'center'
        c.font = "12px monospace"
        c.beginPath()
        data.forEach((d, index) => {
            c.moveTo(left + (index + 1) * 16, bottom)
            c.lineTo(left + (index + 1) * 16, bottom + 8)
            
            var n = Math.floor(d.count * chartH/maxCount)
            
            c.fillStyle = randomColor()
            c.fillRect(left - 5 + (index + 1) * 16, bottom - n, 10, n)
            c.fillStyle = '#000'
            
            c.moveTo(left - 5 + (index + 1) * 16, bottom)
            c.lineTo(left - 5 + (index + 1) * 16, bottom - n)
            c.lineTo(left + 5 + (index + 1) * 16, bottom - n)
            c.lineTo(left + 5 + (index + 1) * 16, bottom)

            if (d.count > 0) {
                c.fillText(d.count, left + (index + 1) * 16, bottom - 8 - n)
            }
            if (d.label == 'd') {
                d.label = '.'
            }
            c.fillText(d.label, left + (index + 1) * 16, bottom + 22)
        })
        c.stroke()
        c.restore()
    }
    
    function drawYLabels (data, maxCount) {
        var coef = Math.floor(chartH/maxCount)
        
        c.save()
        c.textAlign = 'right'
        c.textBaseline = 'middle'
        c.beginPath()
        for (var i = 0; i <= maxCount; i++) {
            var n = i * coef
            if (i > 0 && i % 10 == 0) {
                c.moveTo(left - 5, bottom - n)
                c.lineTo(left, bottom - n)

                c.fillText(i, left - 10, bottom - n)
            }
        }
        c.stroke()
        c.restore()
    }
    
    function drawChart (data) {
        var maxCount = findMaxCount(data)
        
        drawBackground()
        drawXLabels(data, maxCount)
        drawYLabels(data, maxCount)
        drawX()
        drawY()
    }
    
    function drawBar (data) {
        data.label;
        data.count;
    }
	
	function randomColor () {
	    return '#' + ((1 << 24) * Math.random() | 0).toString(16)
	}
})()
