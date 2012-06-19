$(document).ready(function() {
    
    $("#searchButton").click(submitImage);
    
    var canvas, context, tool;
    
    function init() {
        canvas = $("#number")[0];
        if (!canvas) {
            alert('Error: Cannot find the canvas element!');
            return;
        }
        
        if (!canvas.getContext) {
            alert('Error: no canvas.getContext!')
            return;
        }
        
        context = canvas.getContext('2d');
        context.fillStyle = "rgb(128, 128, 128)";
        context.fillRect(0, 0, 200, 200);
        tool = new tool_pencil();
        
        
        canvas.addEventListener('mousedown', ev_canvas, false);
        canvas.addEventListener('mousemove', ev_canvas, false);
        canvas.addEventListener('mouseup', ev_canvas, false);
    }
    
    var started = false;
    
    function relMouseCoords(event){
        var totalOffsetX = 0;
        var totalOffsetY = 0;
        var canvasX = 0;
        var canvasY = 0;
        var currentElement = this;

        do{
            totalOffsetX += currentElement.offsetLeft;
            totalOffsetY += currentElement.offsetTop;
        }
        while(currentElement = currentElement.offsetParent)

        canvasX = event.pageX - totalOffsetX;
        canvasY = event.pageY - totalOffsetY;

        return {x:canvasX, y:canvasY}
    }
    HTMLCanvasElement.prototype.relMouseCoords = relMouseCoords;
            
    function ev_canvas(ev) {
        coords = canvas.relMouseCoords(ev);
        
        ev._x = coords.x;
        ev._y = coords.y;
        
        var func = tool[ev.type];
        if (func) {
            func(ev);
        }
    }
    
    function tool_pencil() {
        var tool = this;
        this.started = false;
        context.strokeStyle = "rgb(255, 255, 255)";
        context.lineWidth = 15.0;
        
        this.mousedown = function(ev) {
            context.beginPath();
            context.moveTo(ev._x, ev._y);
            tool.started = true;
        }
        
        this.mousemove = function(ev) {
            if (tool.started) {
                context.lineTo(ev._x, ev._y);
                context.stroke();
            }
        }
        
        this.mouseup = function(ev) {
            if (tool.started) {
                tool.mousemove(ev);
                tool.started = false;
            }
        }
    }
            
    init();
    
    function showImages(urls, colSize) {
        $("#result").html("");
        for (i=0; i<urls.length; i++) {
            if (i != 0 && i%colSize == 0) {
                $("#result").append("<div id=\"row\">");
            }
            $("#result").append("<span><img src=\"" + urls[i] + "\" width=\"100px\"></img></span>");
            if (i%(colSize-1) == 0) {
                $("#result").append("</div>");
            }
        }
    }
    
    function submitImage() {
        var canvas = $("#number")[0];
        var dataURL = canvas.toDataURL();
        var dataString = dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
        
        $.ajaxSetup ({  
        cache: false  
        });  
        
        $.ajax({
            type: "POST",
            url: "/",
            data: {numberImg : dataString},
            success: function(results) {
                var colSize = 5;
                var urls = results.split(",");
                showImages(urls, colSize);
            }
        });
        
        context.fillRect(0, 0, 200, 200);      
    }    
});
