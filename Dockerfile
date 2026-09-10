# Use official Java 17 image as base
FROM eclipse-temurin:17-jdk-slim-bullseye

# Set working directory
WORKDIR /app

# Copy the JAR file from your local build
COPY target/telegram-bot-1.0-SNAPSHOT.jar /app/app.jar

# Expose any ports if needed (not typically needed for Telegram bots)
# EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "/app/app.ja    r"]