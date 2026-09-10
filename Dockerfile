# Build stage - using a verified working Maven image
FROM maven:3.9.6-eclipse-temurin-17 as build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package

# Final stage - using a verified working Java image
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/target/telegram-bot-1.0-SNAPSHOT.jar /app/app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]