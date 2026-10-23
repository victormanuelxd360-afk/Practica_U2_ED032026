FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY Web/PracticaWeb.csproj Web/
COPY CSharp/Modelos.cs CSharp/
RUN dotnet restore Web/PracticaWeb.csproj
COPY Web/ Web/
RUN dotnet publish Web/PracticaWeb.csproj -c Release --no-restore -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 8080
USER $APP_UID
ENTRYPOINT ["sh", "-c", "exec dotnet PracticaWeb.dll --urls http://0.0.0.0:${PORT:-8080}"]
