#version 330 core

uniform vec2 iResolution; // Resolution of the window
uniform vec2 iPos;        // x, y position of the circle's center
uniform float iRadius;    // Radius of the circle

in vec2 fragmentTexCoord;
out vec4 fragColor;

void main()
{
    // Calculate fragment coordinates in pixels
    vec2 fragCoord = fragmentTexCoord * iResolution;

    // Calculate the center of the circle, flipping the y-coordinate
    vec2 center = vec2(iPos.x, iResolution.y - iPos.y);

    // Calculate distance from the current fragment to the circle center
    vec2 diff = fragCoord - center;
    float dist = length(diff);

    // Determine if this fragment is within the radius of the circle
    if (dist < iRadius/2.5) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red circle
    } else {
        fragColor = vec4(0.0, 0.0, 0.0, 0.0);  // Transparent background
    }
}
