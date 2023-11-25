vertex_shader = '''
#version 450 core

layout (location = 0 ) in vec3 position;
layout (location = 1 ) in vec2 texCoords;
layout (location = 2 ) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec4 newPos = vec4(position.x, position.y, position.z, 1);
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;
}
'''

fragmet_shader = '''
#version 450 core

layout (binding  = 0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals, -dirLight);    
    fragColor = texture(tex, UVs) * max(0, (min(1,intensity)));
}
'''

fragmet_shader1 = '''
#version 450 core

uniform sampler2D particleTexture;
uniform vec3 glowColor;
uniform float glowIntensity;

in vec2 UVs;

out vec4 fragColor;

void main()
{
    vec4 texColor = texture(particleTexture, UVs);

    vec3 glow = glowColor * glowIntensity;

    fragColor = vec4(texColor.rgb + glow, texColor.a);
}
'''

vertex_shader1 = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec3 transformedPosition = position;

    transformedPosition.x += sin(time + position.x);
    transformedPosition.y += cos(time + position.y);

    vec4 newPos = vec4(transformedPosition, 1.0);
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;
}
'''

vertex_shader2 = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec3 shakyPosition = position;
    float amplitude = 0.02;

    shakyPosition += vec3(
        sin(time * 10.0 + position.x),
        cos(time * 10.0 + position.y),
        sin(time * 10.0 + position.z)
    ) * amplitude;

    vec4 newPos = vec4(shakyPosition, 1.0);
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;
}
'''

fragmet_shader2 = '''
#version 450 core

out vec4 fragColor;

uniform float time;

void main()
{
    vec2 uv = gl_FragCoord.xy;
    float offset = 0.01 * uv.x + 0.02 * uv.y;

    vec3 rainbowColor = vec3(
        cos(time + offset * 0.5),
        cos(time + offset * 0.7),
        cos(time + offset * 0.9)
    );

    fragColor = vec4(rainbowColor * 0.5 + 0.5, 1.0);
}
'''

vertex_shader3 = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec3 scaledPosition = position;
    float scaleFactorX = sin(time) * 0.5 + 1.0;
    float scaleFactorY = cos(time) * 0.5 + 1.0;

    scaledPosition.x *= scaleFactorX;
    scaledPosition.y *= scaleFactorY;

    vec4 newPos = vec4(scaledPosition, 1.0);
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;
}
'''

vertex_shader4 = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    vec3 spiraledPosition = position;
    float angle = time * 2.0;

    float radius = length(position.xy);
    spiraledPosition.x = radius * cos(angle);
    spiraledPosition.y = radius * sin(angle);

    vec4 newPos = vec4(spiraledPosition, 1.0);
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * newPos;
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;
}
'''

fragmet_shader3 = '''
#version 450 core

out vec4 fragColor;

uniform float time;

void main()
{
    vec2 uv = gl_FragCoord.xy / vec2(1920, 1080);
    float noise = fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453);

    vec3 errorColor = vec3(
        1.0,
        0.0,
        0.0
    );

    fragColor = vec4(errorColor * noise, 1.0);
}
'''

fragmet_shader4 = '''
#version 450 core

out vec4 fragColor;

uniform vec3 dirLight;
uniform float time;

in vec3 outNormals;

void main()
{

    vec3 norm = normalize(outNormals);
    vec3 lightDir = normalize(dirLight);

  
    float diff = max(dot(norm, lightDir), 0.0);


    if (diff > 0.9) {
        diff = 1.0;
    } else if (diff > 0.6) {
        diff = 0.8;
    } else if (diff > 0.3) {
        diff = 0.5;
    } else {
        diff = 0.2;
    }

    vec3 baseColor = vec3(0.5 + 0.1 * diff, 0.5 + 0.1 * diff, 0.5 + 0.1 * diff);

    fragColor = vec4(baseColor, 1.0);
}

'''