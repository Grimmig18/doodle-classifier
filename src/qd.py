"""
Taken from https://github.com/martinohanlon/quickdraw_python
Paritally modified to suit the needs of our projects.
"""


from PIL import Image, ImageDraw
import numpy as np

class QuickDrawing():
    """
    Represents a single Quick, Draw! drawing.
    """
    def __init__(self, name, drawing_data):
        self._name =name
        self._drawing_data = drawing_data
        self._strokes = None
        self._image = None


    @property
    def image_data(self):
        """
        Returns the raw image data as list of strokes with a list of X 
        co-ordinates and a list of Y co-ordinates.
        Co-ordinates are aligned to the top-left hand corner with values
        from 0 to 255.
        See https://github.com/googlecreativelab/quickdraw-dataset#simplified-drawing-files-ndjson
        for more information regarding how the data is represented.
        """
        return self._drawing_data["image"]
    
    @property
    def strokes(self):
        """
        Returns a list of pen strokes containing a list of (x,y) coordinates which make up the drawing.
        To iterate though the strokes data use::
        
            from quickdraw import QuickDrawData
            qd = QuickDrawData()
            anvil = qd.get_drawing("anvil")
            for stroke in anvil.strokes:
                for x, y in stroke:
                    print("x={} y={}".format(x, y)) 
        """
        # load the strokes
        if self._strokes is None:
            max_x, _, max_y, _, a = self.get_rescale_factors(self.image_data)
            
            self._strokes = []
            for stroke in self.image_data:
                points = []

                stroke[0] = [x for x in np.rint(np.interp(stroke[0], (max_x - a, max_x), (0, 255))).tolist()]
                stroke[1] = [y for y in np.rint(np.interp(stroke[1], (max_y - a, max_y), (0, 255))).tolist()]

                xs = stroke[0]
                ys = stroke[1]

                if len(xs) != len(ys):
                    raise Exception("something is wrong, different number of x's and y's")

                for point in range(len(xs)):
                    x = xs[point]
                    y = ys[point]
                    points.append((x,y))
                self._strokes.append(points)


        return self._strokes

    @property
    def image(self):
        """
        Returns a `PIL Image <https://pillow.readthedocs.io/en/3.0.x/reference/Image.html>`_ 
        object of the drawing on a white background with a black drawing. Alternative image
        parameters can be set using ``get_image()``.
        To save the image you would use the ``save`` method::
            from quickdraw import QuickDrawData
            qd = QuickDrawData()
            anvil = qd.get_drawing("anvil")
            anvil.image.save("my_anvil.gif")
            
        """
        if self._image is None:
            self._image = self.get_image()

        return self._image

    def get_image(self, stroke_color=(0,0,0), stroke_width=2, bg_color=(255,255,255)):
        """
        Get a `PIL Image <https://pillow.readthedocs.io/en/3.0.x/reference/Image.html>`_ 
        object of the drawing.
        :param list stroke_color:
            A list of RGB (red, green, blue) values for the stroke color,
            defaults to (0,0,0).
        :param int stroke_color:
            A width of the stroke, defaults to 2.
        :param list bg_color:
            A list of RGB (red, green, blue) values for the background color,
            defaults to (255,255,255).
        """
        image = Image.new("RGB", (256,256), color=bg_color)
        image_draw = ImageDraw.Draw(image)

        for stroke in self.strokes:
            image_draw.line(stroke, fill=stroke_color, width=stroke_width)

        return image

    def get_rescale_factors(self, strokes): 
        """
        Get the max and min x and y value of a given image, by processing its strokes
        a is the side length of a square perfectly fitting the given image
        """

        # Initialize the return valoes with smallest possible / largest possible values
        max_x = 0
        min_x = np.inf

        max_y = 0
        min_y = np.inf

        a = 0

        # Loop trhough all strokes to find min / max values
        for stroke in strokes:

            # Potential new min / max
            _max_x = max(stroke[0])
            _min_x = min(stroke[0])

            # If new min / max is found, assign to global min / max of drawing
            if _max_x > max_x:
                max_x = _max_x

            if _min_x < min_x:
                min_x = _min_x

            # Potential new min / max
            _max_y = max(stroke[1])
            _min_y = min(stroke[1])

            if _max_y > max_y:
                max_y = _max_y

            if _min_y < min_y:
                min_y = _min_y
            
        # Caluclate the side length of a square perfectly fitting the drawing
        _a = max_x - min_x
        if max_y - min_y > a:
            a = max_y - min_y

        if _a > a:
            a = _a

        return max_x, min_x, max_y, min_y, a

    # @staticmethod
    # def tupels_to_arrays(tupel_arrays):
    #     """
    #     Takes an list of strokes, each represented as a list of (x, y) tupels and converts them into  
    #     """
    #     strokes = [[], []]
    #     for arr in tupel_arrays:
    #         for t in arr:
    #            strokes[0].append(int(t[0]))
    #            strokes[1].append(int(t[1])) 
        
    #     return strokes


    @staticmethod
    def image_to_stroke_array(image, dim=256, background=[255,255,255]):
        """
        
        """
        stroke = [[], []]
        image = np.reshape(image, (dim, dim, 3))
        for x in range(len(image)):
            for y in range(len(image[x])):
                if (image[x,y]!=background).any():
                    stroke[0].append(x)
                    stroke[1].append(y)

        return stroke
    

    def __str__(self):
        return "QuickDrawing key_id={}".format(self.key_id)