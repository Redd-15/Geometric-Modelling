const POINT_RADIUS = 10;

/**
 * A panel for drawing splines.
 */
class SplinePanel extends Panel {
    /**
     * Construct a new spline panel.
     */
    constructor(mock) {
        super();
        this._points = [
            { x: 100, y: 100 },
            { x: 200, y: 200 },
            { x: 200, y: 400 },
            { x: 400, y: 500 },
            { x: 500, y: 400 },
            { x: 600, y: 100 },
        ];
        this._selectedPoint = null;
        this._slider = document.getElementById("tSlider");
    }

    /**
     * Handle the mouse down event.
     */
    onMouseDown(mouse) {
        this._selectedPoint = this.findPoint(mouse.x, mouse.y);
    }

    /**
    * Handle the mouse move event.
    */
    onMouseMove(mouse) {
        if (this._selectedPoint != null) {
            this._selectedPoint.x = mouse.x;
            this._selectedPoint.y = mouse.y;
        }
        this.requireRedraw();
    }

    /**
     * Handle the mouse up event.
     */
    onMouseUp(mouse) {
        this._selectedPoint = null;
    }

    /**
     * Find a control point at the given coordinates.
     */
    findPoint(x, y) {
        for (var point of this._points) {
            const dx = point.x - x;
            const dy = point.y - y;
            let distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < POINT_RADIUS) {
                return point;
            }
        }
        return null;
    }

    /**
     * Draw the content of the panel.
     */
    draw(context) {
        context.fillStyle = "#FFF";
        context.fillRect(0, 0, this.width, this.height);
        this.drawPoints(context, this._points);
        this.draw2dFunction(context, 0, 1, 1 / 1000, t => this.deCasteljauApproximation(this._points, t).x, t => this.deCasteljauApproximation(this._points, t).y, "#FF00FF");
        this.deCasteljauIteration(context);
    }

    // Lesson 2 Lagrange interpolation
    lagrangeInterpolation(t) {
        let tValues = Array.from({ length: this._points.length }, (_, i) => i);
        //this._points.sort((a, b) => a.x - b.x);
        let result = { x: 0, y: 0 };

        for (let i = 0; i < this._points.length; i++) {
            let term = { x: this._points[i].x, y: this._points[i].y };
            let li = 1;

            for (let j = 0; j < this._points.length; j++) {
                if (i !== j) {
                    li *= (t - tValues[j]) / (tValues[i] - tValues[j]);
                }
            }

            result.x += term.x * li;
            result.y += term.y * li;
        }

        return result;
    }

    //Lesson 3 de Casteljau iteration, Bezier curve
    deCasteljauIteration(context) {
        let t = this._slider.value;
        let iterationControl = structuredClone(this._points);


        for (let i = 0; i < this._points.length; i++) {
            let newControlPoints = [];
            for (let j = 1; j < iterationControl.length; j++) {
                this.drawSegment(iterationControl[j - 1], iterationControl[j]);
                newControlPoints.push({
                    x: (1 - t) * iterationControl[j - 1].x + t * iterationControl[j].x,
                    y: (1 - t) * iterationControl[j - 1].y + t * iterationControl[j].y
                });
            }
            if (i == this._points.length - 1) this.drawPoints(context, iterationControl, "#FF0000");
            else if (i > 0) this.drawPoints(context, iterationControl, "#00FF00");
            iterationControl = newControlPoints;
        }
        return iterationControl[0];
    }

    deCasteljauApproximation(points, t) {
        if (points.length === 1) {
            return points[0];
        }
        let newPoints = [];
        for (let i = 0; i < points.length - 1; i++) {
            let x = (1 - t) * points[i].x + t * points[i + 1].x;
            let y = (1 - t) * points[i].y + t * points[i + 1].y;
            newPoints.push({ x, y });
        }
        return this.deCasteljauApproximation(newPoints, t);
    }

    drawSegment(point1, point2) {
        context.strokeStyle = "#D3D3D3";
        context.beginPath();
        context.moveTo(point1.x, point1.y);
        context.lineTo(point2.x, point2.y);
        context.stroke();
        context.closePath();
    }

    draw2dFunction(context, min, max, step, x_fun, y_fun, colour = "#00FF00") {
        let t = min;
        context.strokeStyle = colour;
        context.beginPath();
        context.moveTo(x_fun(t), y_fun(t));
        while (t <= max) {
            let x = x_fun(t);
            let y = y_fun(t);
            context.lineTo(x, y);
            t += step;
        }
        context.stroke();
        context.closePath();
    }

    /**
     * Draw the control points.
     */
    drawPoints(context, points, colour = "#00F") {
        for (const point of points) {
            this.drawPoint(context, point, colour);
        }
    }

    /**
     * Draw a control point.
     */
    drawPoint(context, point, colour = "#00F") {
        context.strokeStyle = colour;
        context.beginPath();
        context.moveTo(point.x - POINT_RADIUS, point.y);
        context.lineTo(point.x + POINT_RADIUS, point.y);
        context.stroke()
        context.beginPath();
        context.moveTo(point.x, point.y - POINT_RADIUS);
        context.lineTo(point.x, point.y + POINT_RADIUS);
        context.stroke()
    }
}

