#version 330 core

uniform vec2 iResolution; // Resolution of the window
uniform vec2 iPos;        // x, y position of the circle's center
uniform float iRadius;    // Radius of the ring
uniform float iBlur;      // Blur width
uniform vec4 iColor;      // Color of the ring (RGBA)

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

    // Create a blurred ring effect using smoothstep
    float radius = iRadius/1.8;  // Radius of the ring
    float innerRadius = radius - iBlur;  // Inner radius for the ring
    float outerRadius = radius + iBlur;  // Outer radius for the ring

    // Use smoothstep to create a soft transition between inner and outer radius
    float alphaInner = smoothstep(innerRadius, innerRadius + iBlur, dist);
    float alphaOuter = smoothstep(outerRadius - iBlur, outerRadius, dist);

    // Combine the two alpha values to create a ring shape
    float alpha = alphaInner * (1.0 - alphaOuter);

    // Set color based on alpha value and iColor
    fragColor = iColor * alpha;  // Ring with transparency and custom color
}