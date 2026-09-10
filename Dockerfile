# Build stage - uses Maven image that includes Java 17 and Maven
FROM maven:3.8.6-openjdk-17-slim as build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package

# Final stage - use specific OS version tag
FROM maven:3.8.6-openjdk-17-slim
WORKDIR /app
COPY --from=build /app/target/telegram-bot-1.0-SNAPSHOT.jar /app/app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]