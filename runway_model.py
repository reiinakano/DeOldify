# MIT License

# Copyright (c) 2019 Runway AI, Inc

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import runway
from runway.data_types import number, image

from fasterai.visualize import get_image_colorizer

# Setup the model, initialize weights, set the configs of the model, etc.
# Every model will have a different set of configurations and requirements.
# Check https://docs.runwayapp.ai/#/python-sdk to see a complete list of
# supported configs. The setup function should return the model ready to be
# used.
@runway.setup()
def setup(opts):
    colorizer = get_image_colorizer(artistic=True)
    return colorizer


# Every model needs to have at least one command. Every command allows to send
# inputs and process outputs. To see a complete list of supported inputs and
# outputs data types: https://sdk.runwayml.com/en/latest/data_types.html
@runway.command(name='generate',
                inputs={ 'image': image(),
                         'render_factor': number(min=7, max=45, step=1, default=35) },
                outputs={ 'image': image() })
def generate(model, args):
    render_factor = args['render_factor']
    print('[GENERATE] Ran with render_factor "{}"'.format(render_factor))

    orig_image = args['image'].convert('RGB')
    model._clean_mem()
    output_image = model.filter.filter(orig_image, orig_image, render_factor=render_factor)

    return {
        'image': output_image
    }


if __name__ == '__main__':
    # run the model server using the default network interface and ports,
    # displayed here for convenience
    runway.run(host='0.0.0.0', port=8000)

## Now that the model is running, open a new terminal and give it a command to
## generate an image. It will respond with a base64 encoded URI
# curl \
#   -H "content-type: application/json" \
#   -d '{ "caption": "red" }' \
#   localhost:8000/generate
