if (window.addEventListener) {
    window.addEventListener('load', function () {
        var canvas, context, tool;
        
        function init() {
            canvas = document.getElementById('number');
            if (!canvas) {
                alert('Error: Cannot find the canvas element!');
                return;
            }
            
            if (!canvas.getContext) {
                alert('Error: no canvas.getContext!')
                return;
            }
            
            context = canvas.getContext('2d');
            tool = new tool_pencil();
            
            canvas.addEventListener('mousedown', ev_canvas, false);
            canvas.addEventListener('mousemove', ev_canvas, false);
            canvas.addEventListener('mouseup', ev_canvas, false);
        }
        
        var started = false;
        
        function ev_canvas(ev) {
             if (ev.layerX || ev.layerX == 0) { // Firefox
                ev._x = ev.layerX;
                ev._y = ev.layerY;
            } else if (ev.offsetX || ev.offsetX == 0) {  // Opera
                ev._x = ev.offsetX;
                ev._y = ev.offsetY;
            }
            
            var func = tool[ev.type];
            if (func) {
                func(ev);
            }
        }
        
        function tool_pencil() {
            var tool = this;
            this.started = false;
            context.lineWidth = 20.0;
            
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
    }, false); }
    
function submitImage() {
    canvas = document.getElementById('number');
    var dataURL = canvas.toDataURL();
    
    var form = document.createElement("form");
    form.setAttribute("method", "post");
    form.setAttribute("action", "/");
    
    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "numberImg");
    var data = dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
    hiddenField.setAttribute("value", data);
    
    form.appendChild(hiddenField);
    form.submit();
}
