# Build stage
FROM eclipse-temurin:17-jdk-slim as build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package

# Final stage
FROM eclipse-temurin:17-jdk-slim
WORKDIR /app
COPY --from=build /app/target/telegram-bot-1.0-SNAPSHOT.jar /app/app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]