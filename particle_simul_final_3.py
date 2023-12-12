import pygame
import sys
import math
import random

# Pygame 초기화
pygame.init()

# 화면 설정
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fluid Simulator")

# 색깔 정의
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# 유체 입자 설정
class FluidParticle:
    def __init__(self, x, y, size, color, velocity):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.velocity = velocity
        self.mass = math.pi * size ** 2  # 질량은 입자의 크기에 비례

    def update(self, mouse_position=None):
        # 중력에 따라 속도 업데이트 (중력 제거)
        # gravity = 0.1
        # self.velocity[1] += gravity

        # 마우스 인력 적용
        if mouse_position:
            dx = mouse_position[0] - self.x
            dy = mouse_position[1] - self.y
            distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

            attraction_force = 2  # Adjust attraction strength as needed
            angle = math.atan2(dy, dx)

            self.velocity[0] += attraction_force * math.cos(angle)
            self.velocity[1] += attraction_force * math.sin(angle)

        # 속도에 따라 위치 업데이트
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # 화면 경계에서 반사 (탄성력을 낮춤)
        restitution = 0.9  # 반발력 계수를 조절
        if self.x < self.size or self.x > width - self.size:
            self.velocity[0] *= -restitution
            # 화면 경계에서 벗어나지 않도록 위치 조정
            self.x = max(self.size, min(self.x, width - self.size))
        if self.y < self.size or self.y > height - self.size:
            self.velocity[1] *= -restitution
            # 화면 경계에서 벗어나지 않도록 위치 조정
            self.y = max(self.size, min(self.y, height - self.size))

# 빨간색 유체 입자 설정
class RedFluidParticle(FluidParticle):
    def __init__(self, x, y, size, velocity):
        super().__init__(x, y, size, red, velocity)

    def apply_repulsion(self, other_particle):
        dx = self.x - other_particle.x
        dy = self.y - other_particle.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        repulsion_force = 200 / distance ** 2  # Adjust repulsion strength as needed
        angle = math.atan2(dy, dx)

        self.velocity[0] += repulsion_force * math.cos(angle) / self.mass
        self.velocity[1] += repulsion_force * math.sin(angle) / self.mass


# 파란색 유체 입자 설정
class BlueFluidParticle(FluidParticle):
    def __init__(self, x, y, size, velocity):
        super().__init__(x, y, size, blue, velocity)


    def apply_self_viscosity(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        viscosity_force = 50  # Adjust viscosity strength as needed
        angle = math.atan2(dy, dx)

        self.velocity[0] += viscosity_force * math.cos(angle) / self.mass
        self.velocity[1] += viscosity_force * math.sin(angle) / self.mass


    def apply_viscosity(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        viscosity_force = 10  # Adjust viscosity strength as needed
        angle = math.atan2(dy, dx)

        self.velocity[0] += viscosity_force * math.cos(angle) / self.mass
        self.velocity[1] += viscosity_force * math.sin(angle) / self.mass

# 초록색 유체 입자 설정
class GreenFluidParticle(FluidParticle):
    def __init__(self, x, y, size, velocity):
        super().__init__(x, y, size, green, velocity)

    def apply_attraction(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        attraction_force = 40  # Adjust attraction strength as needed
        angle = math.atan2(dy, dx)

        self.velocity[0] += attraction_force * math.cos(angle) / self.mass
        self.velocity[1] += attraction_force * math.sin(angle) / self.mass

    def apply_repulsion(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        repulsion_force = 1  # Adjust repulsion strength as needed
        angle = math.atan2(dy, dx)

        self.velocity[0] -= repulsion_force * math.cos(angle) / self.mass # Negative sign for attraction
        self.velocity[1] -= repulsion_force * math.sin(angle) / self.mass # Negative sign for attraction

# 흰색 유체 입자 설정
class WhiteFluidParticle(FluidParticle):
    def __init__(self, x, y, size, velocity):
        super().__init__(x, y, size, (255, 255, 255), velocity)

    def apply_self_viscosity(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        viscosity_force = 1000  # Increase viscosity strength
        angle = math.atan2(dy, dx)

        self.velocity[0] += viscosity_force * math.cos(angle) / self.mass
        self.velocity[1] += viscosity_force * math.sin(angle) / self.mass

    def apply_attraction(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        attraction_force = 10  # Adjust attraction strength as needed
        angle = math.atan2(dy, dx)

        self.velocity[0] += attraction_force * math.cos(angle) / self.mass
        self.velocity[1] += attraction_force * math.sin(angle) / self.mass

    def apply_viscosity(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        viscosity_force = 5  # Increase viscosity strength
        angle = math.atan2(dy, dx)

        self.velocity[0] += viscosity_force * math.cos(angle) / self.mass
        self.velocity[1] += viscosity_force * math.sin(angle) / self.mass

    def apply_repulsion(self, other_particle):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

        repulsion_force = 0.005  # Decrease repulsion strength
        angle = math.atan2(dy, dx)

        self.velocity[0] -= repulsion_force * math.cos(angle) / self.mass # Negative sign for attraction
        self.velocity[1] -= repulsion_force * math.sin(angle) / self.mass # Negative sign for attraction


# 충돌 보정 함수 수정
def resolve_collision(particle1, particle2):
    dx = particle1.x - particle2.x
    dy = particle1.y - particle2.y
    distance = max(1, math.sqrt(dx ** 2 + dy ** 2))  # Avoid division by zero

    overlap = (particle1.size + particle2.size) - distance
    if overlap > 0:
        angle = math.atan2(dy, dx)

        # 상대 속도 계산
        relative_velocity_x = particle2.velocity[0] - particle1.velocity[0]
        relative_velocity_y = particle2.velocity[1] - particle1.velocity[1]

        # 상대 속도와 충돌 방향의 내적
        dot_product = (relative_velocity_x * (particle2.x - particle1.x) +
                       relative_velocity_y * (particle2.y - particle1.y))

        # 질량으로 나누어 운동량 보존 법칙 적용
        impulse = 2.0 * dot_product / (particle1.mass + particle2.mass)

        # 입자의 속도 갱신
        particle1.velocity[0] += impulse * (particle2.x - particle1.x) / distance / particle1.mass
        particle1.velocity[1] += impulse * (particle2.y - particle1.y) / distance / particle1.mass
        particle2.velocity[0] -= impulse * (particle2.x - particle1.x) / distance / particle2.mass
        particle2.velocity[1] -= impulse * (particle2.y - particle1.y) / distance / particle2.mass

        # 충돌 시 위치 조정
        particle1.x += overlap / 2 * math.cos(angle)
        particle1.y += overlap / 2 * math.sin(angle)
        particle2.x -= overlap / 2 * math.cos(angle)
        particle2.y -= overlap / 2 * math.sin(angle)

# 유체 초기화
num_blue_particles = 25
num_red_particles = 25
num_green_particles = 10
num_white_particles = 3

# num_blue_particles = 1
# num_red_particles = 1
# num_green_particles = 1
# num_white_particles = 1


blue_particles = [BlueFluidParticle(
    x=random.randint(50, width - 50),
    y=random.randint(50, height - 50),
    size=10,
    velocity=[random.uniform(-1, 1), random.uniform(-1, 1)]
) for _ in range(num_blue_particles)]

red_particles = [RedFluidParticle(
    x=random.randint(50, width - 50),
    y=random.randint(50, height - 50),
    size=10,
    velocity=[random.uniform(-1, 1), random.uniform(-1, 1)]
) for _ in range(num_red_particles)]

green_particles = [GreenFluidParticle(
    x=random.randint(50, width - 50),
    y=random.randint(50, height - 50),
    size=20,  # 빨간색과 파란색 입자의 크기의 두 배
    velocity=[random.uniform(-1, 1), random.uniform(-1, 1)]
) for _ in range(num_green_particles)]


white_particles = [WhiteFluidParticle(
    x=random.randint(50, width - 50),
    y=random.randint(50, height - 50),
    size=40,  # 초록색 입자의 크기의 두 배
    velocity=[random.uniform(-1, 1), random.uniform(-1, 1)]
) for _ in range(num_white_particles)]


# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 마우스 좌표 가져오기
    mouse_position = pygame.mouse.get_pos()

    # 마우스 클릭 상태 확인
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # 유체 상태 갱신
    # 파란색 입자 상태 갱신 
    for blue_particle in blue_particles:
        blue_particle.update(mouse_position if mouse_pressed else None)

        # Apply self viscosity to other blue particles
        for other_blue_particle in blue_particles:
            if other_blue_particle != blue_particle:
                blue_particle.apply_self_viscosity(other_blue_particle)




    for red_particle in red_particles:
        red_particle.update(mouse_position if mouse_pressed else None)

        # Apply repulsion to other red particles
        for other_red_particle in red_particles:
            if other_red_particle != red_particle:
                red_particle.apply_repulsion(other_red_particle)

        # Apply viscosity to red particles
        for other_red_particle in red_particles:
            if other_red_particle != red_particle:
                blue_particle.apply_viscosity(other_red_particle)

        # Apply viscosity to blue particles
        for blue_particle in blue_particles:
            if blue_particle != red_particle:
                blue_particle.apply_viscosity(red_particle)

    for green_particle in green_particles:
        green_particle.update(mouse_position if mouse_pressed else None)

        # Apply attraction to red particles
        for red_particle in red_particles:
            green_particle.apply_attraction(red_particle)

        # Apply attraction to blue particles
        for blue_particle in blue_particles:
            green_particle.apply_attraction(blue_particle)

        # Apply repulsion to other green particles
        for other_green_particle in green_particles:
            if other_green_particle != green_particle:
                green_particle.apply_repulsion(other_green_particle)

    # 흰색 입자 상태 갱신
    for white_particle in white_particles:
        white_particle.update(mouse_position if mouse_pressed else None)


        # Apply self viscosity to other white particles
        for other_white_particle in white_particles:
            if other_white_particle != white_particle:
                white_particle.apply_self_viscosity(other_white_particle)

        # Apply attraction to red particles
        for red_particle in red_particles:
            white_particle.apply_attraction(red_particle)

        # Apply attraction to blue particles
        for blue_particle in blue_particles:
            white_particle.apply_attraction(blue_particle)

        # Apply attraction to green particles
        for green_particle in green_particles:
            white_particle.apply_attraction(green_particle)

        # Apply viscosity to all particles
        for particle in blue_particles + red_particles + green_particles:
            white_particle.apply_viscosity(particle)

        # Apply repulsion to all particles
        for particle in blue_particles + red_particles + green_particles:
            white_particle.apply_repulsion(particle)


    # 충돌 보정
    for i in range(len(blue_particles + red_particles + green_particles + white_particles) - 1):
        for j in range(i + 1, len(blue_particles + red_particles + green_particles + white_particles)):
            resolve_collision(
                (blue_particles + red_particles + green_particles + white_particles)[i],
                (blue_particles + red_particles + green_particles + white_particles)[j]
            )





    # 화면 그리기
    screen.fill(black)

    # 파란색 입자 그리기
    for blue_particle in blue_particles:
        pygame.draw.circle(screen, blue_particle.color, (int(blue_particle.x), int(blue_particle.y)), blue_particle.size)

    # 빨간색 입자 그리기
    for red_particle in red_particles:
        pygame.draw.circle(screen, red_particle.color, (int(red_particle.x), int(red_particle.y)), red_particle.size)

    # 초록색 입자 그리기
    for green_particle in green_particles:
        pygame.draw.circle(screen, green_particle.color, (int(green_particle.x), int(green_particle.y)), green_particle.size)

 # 흰색 입자 그리기
    for white_particle in white_particles:
        pygame.draw.circle(screen, white_particle.color, (int(white_particle.x), int(white_particle.y)), white_particle.size)


    pygame.display.flip()
    pygame.time.Clock().tick(60)