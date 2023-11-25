import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import math

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.clearColor = [0,0,0]

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glViewport(0,0, self.width, self.height)

       
        self.elapsedTime  = 0.0
        self.target=glm.vec3(0,0,0)
        self.filledMode=True
        self.cameraAngle = 0
        self.cameraHeightOffset = 0
        self.cameraFOV = 60  
        self.cameraDistance = 10  
        self.cameraAngle = 0
        self.cameraHeightOffset = 0
        self.cameraFOV = 60  
        self.minDistance = 5
        self.maxDistance = 20
        self.minHeight = -5
        self.maxHeight = 5
        self.minFOV = 20
        self.maxFOV = 80

        self.scene = []
        self.activeShader = None
        
        self.dirLight = glm.vec3(1,1,-1)
        self.camPosition = glm.vec3(0, -8, 0)  
        self.camRotation = glm.vec3(0, 0, 0)  
        self.target = glm.vec3(0, 0, 0)      
        self.getViewMatrix=self.getViewMatrix()
        self.projectionMatrix = glm.perspective(glm.radians(60), 
                                                self.width/self.height, 
                                                0.1, 
                                                1000) 
    

    def toggleFilledMode(self):
        self.filledMode=not self.filledMode
        if self.filledMode:
            glEnable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT,GL_FILL)
        else:
            glDisable(GL_CULL_FACE)
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)

    def getViewMatrix(self):
        identity = glm.mat4(1)

        translateMat = glm.translate(identity, self.camPosition)

        pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1,0,0)) 
        yaw = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0,1,0)) 
        roll = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0,0,1)) 

        rotationMat = pitch * yaw * roll

        camMatrix = translateMat * rotationMat

        return  glm.inverse(camMatrix)
    
    def changeClearColor(self, color):
        self.clearColor = color
    
    def setShader(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.activeShader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER), compileShader(fragmentShader, GL_FRAGMENT_SHADER))
        else: 
            self.activeShader = None
    def update(self):
        self.getViewMatrix=glm.lookAt(self.camPosition,self.target,glm.vec3(0,1,0.95))
        cameraRelPos = glm.vec3(
            self.cameraDistance * math.sin(self.cameraAngle),
            self.cameraHeightOffset,
            self.cameraDistance * math.cos(self.cameraAngle)
        )

  
        self.getViewMatrix = glm.lookAt(self.camPosition + cameraRelPos, self.target, glm.vec3(0, 1, 0))


        self.projectionMatrix = glm.perspective(glm.radians(self.cameraFOV), self.width / self.height, 0.1, 1000)

    def rotateCamera(self, delta_angle):
        self.cameraAngle += delta_angle

    def zoomCamera(self, delta_zoom):
        self.cameraFOV = max(self.minFOV, min(self.maxFOV, self.cameraFOV + delta_zoom))

    def moveCameraVertical(self, delta_height):
        self.cameraHeightOffset = max(self.minHeight, min(self.maxHeight, self.cameraHeightOffset + delta_height))


    def render(self):
        glClearColor(self.clearColor[0], self.clearColor[1], self.clearColor[2], 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        if self.activeShader is not None:
            glUseProgram(self.activeShader)

            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "viewMatrix"), 1, GL_FALSE, glm.value_ptr(self.getViewMatrix))

            glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "projectionMatrix"), 1, GL_FALSE, glm.value_ptr(self.projectionMatrix))


            glUniform1f(glGetUniformLocation(self.activeShader, "time"), self.elapsedTime  )
            
            glUniform3fv( glGetUniformLocation (self.activeShader, "dirLight"), 1, glm.value_ptr(self.dirLight))

            

        for obj in self.scene:
            if self.activeShader is not None:
                glUniformMatrix4fv(glGetUniformLocation(self.activeShader, "modelMatrix"), 1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))


            obj.render()

