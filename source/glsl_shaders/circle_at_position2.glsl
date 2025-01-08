#version 330 core

uniform vec2 iResolution;
uniform vec4 iRect;  // x, y, width, height
uniform float iRadius;

in vec2 fragmentTexCoord;
out vec4 fragColor;

vec2 calculateCenter(vec4 rect, vec2 resolution) {
    float centerX = rect.x + rect.z / 2.0;
    float centerY = resolution.y - (rect.y + rect.w / 2.0);
    return vec2(centerX, centerY);
}

void main()
{
    vec2 fragCoord = fragmentTexCoord * iResolution;
    vec2 center = calculateCenter(iRect, iResolution);

    vec2 diff = fragCoord - center;
    float dist = length(diff);

    if (dist < iRadius) {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red circle
    } else {
        fragColor = vec4(0.0, 0.0, 0.0, 0.0);  // Transparent background
    }
}
