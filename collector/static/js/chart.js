(function () {
    var canvas = document.createElement('canvas')
    canvas.width = 1360
    canvas.height = 550
    canvas.className = 'chart'
    
    var chartW = 1240,
        chartH = 410,
        left = 80,
        bottom = 500,
        barWidth = 42;
    
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
        var m = 0
        data.forEach(d => {
            m = Math.max(m, d.count)
        })
        return m
    }
    
    function drawBackground () {
        c.save()
        c.fillStyle = '#f0f0f0'
        c.fillRect(0, 0, canvas.width, canvas.height)
        c.fillStyle = '#000'
        c.textAlign = 'center'
        c.fillText('OCR training data ' + formatDate(new Date()), canvas.width / 2, 20)
        c.restore()
    }
    
    function drawX () {
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
        c.beginPath()
        data.forEach((d, index) => {
            var x = (index + 1) * barWidth / 2;
            var b = barWidth / 6;

            c.moveTo(left + x, bottom)
            c.lineTo(left + x, bottom + 8)
            
            var n = Math.floor(d.count * chartH/maxCount)
            
            c.fillStyle = randomColor()
            c.fillRect(left - b + x, bottom - n, b * 2, n)
            c.fillStyle = '#000'
            
            c.moveTo(left - b + x, bottom)
            c.lineTo(left - b + x, bottom - n)
            c.lineTo(left + b + x, bottom - n)
            c.lineTo(left + b + x, bottom)

            if (d.count > 0) {
                if (d.count > 999) {
                    c.font = '9px monospace'
                } else {
                    c.font = '11px monospace'
                }
                c.fillText(d.count, left + x, bottom - 8 - n)
            }
            if (d.label == 'd') {
                d.label = '.'
            }
            c.font = '12px monospace'
            c.fillText(d.label, left + x, bottom + 22)
        })
        c.stroke()
        c.restore()
    }
    
    function drawYLabels (data, maxCount) {
        var coef = Math.floor((chartH/maxCount) * 10) / 10
        var p = Math.floor(Math.log10(maxCount))
        var step = Math.pow(10, p)
        
        c.save()
        c.textAlign = 'right'
        c.textBaseline = 'middle'
        c.beginPath()
        
        var i = 1;
        while(i * step < maxCount) {
            var y = i * step * coef
            
            c.moveTo(left - 5, bottom - y)
            c.lineTo(left, bottom - y)

            c.fillText(i * step, left - 10, bottom - y)
            i++;
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
    
    function randomColor () {
        return '#' + ((1 << 24) * Math.random() | 0).toString(16)
    }
    
    function formatDate (date) {
        var arr = [date.getDate(), date.getMonth() + 1, date.getFullYear()]
        return arr.map(d => {
            return padZero(d)
        }).join('/')
    }
    
    function padZero (n) {
        return n > 9 ? n : '0' + n
    }
})()
