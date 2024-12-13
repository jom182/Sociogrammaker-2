import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import json
import uuid

# Global storage for responses (simulates a database)
responses = {}

def collect_student_input():
    """Collect input from students securely."""
    st.header("Student Input")
    student_id = st.text_input("Enter your student ID:")

    if student_id:
        preferences = st.text_area("Enter the names of classmates you prefer to work with (comma-separated):")
        if st.button("Submit Preferences"):
            responses[student_id] = [name.strip() for name in preferences.split(",") if name.strip()]
            st.success("Your response has been recorded. Thank you!")

def mentor_view():
    """Allow the mentor to analyze and visualize the sociogram."""
    st.header("Mentor Dashboard")
    mentor_id = st.text_input("Enter your mentor ID to access the dashboard:", type="password")

    if mentor_id == "mentor123":  # Replace with secure authentication in production
        if st.button("Generate Sociogram"):
            data = responses  # Use the collected responses

            # Step 2: Create sociogram
            G = create_sociogram(data)

            # Step 3: Analyze sociogram
            analysis = analyze_sociogram(G)

            # Step 4: Visualize sociogram
            st.subheader("Sociogram Visualization")
            visualize_sociogram(G)

            # Step 5: Display report
            st.subheader("Sociogram Analysis Report")
            report = generate_report(analysis)
            st.text(report)

            # Allow download of the report
            st.download_button("Download Report", report, file_name="sociogram_report.txt")
    else:
        st.warning("Please enter a valid mentor ID.")

def create_sociogram(data):
    """Generate a sociogram based on student preference data."""
    G = nx.DiGraph()

    # Add edges based on preferences
    for student, preferences in data.items():
        for peer in preferences:
            G.add_edge(student, peer)

    return G

def analyze_sociogram(G):
    """Provide analysis of the sociogram."""
    analysis = {
        "popular_students": sorted(G.in_degree, key=lambda x: x[1], reverse=True),
        "isolated_students": [node for node in G.nodes if G.degree(node) == 0],
        "clusters": list(nx.weakly_connected_components(G))
    }
    return analysis

def visualize_sociogram(G):
    """Generate and return a sociogram visualization as a Streamlit figure."""
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightblue")

    # Draw edges
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    plt.title("Sociogram", fontsize=16)
    plt.axis("off")

    st.pyplot(plt)

def generate_report(analysis):
    """Generate a textual summary of the sociogram analysis."""
    report = []

    # Popular students
    report.append("Popular students (most chosen):")
    for student, score in analysis["popular_students"][:5]:
        report.append(f"- {student}: chosen {score} times")

    # Isolated students
    report.append("\nIsolated students (no connections):")
    for student in analysis["isolated_students"]:
        report.append(f"- {student}")

    # Clusters
    report.append("\nClusters in the class:")
    for i, cluster in enumerate(analysis["clusters"], 1):
        report.append(f"- Cluster {i}: {', '.join(cluster)}")

    return "\n".join(report)

def main():
    st.title("Classroom Sociogram Tool")
    st.write("This tool helps students securely submit preferences and mentors analyze social dynamics.")

    user_role = st.radio("Select your role:", ["Student", "Mentor"])

    if user_role == "Student":
        collect_student_input()
    elif user_role == "Mentor":
        mentor_view()

if __name__ == "__main__":
    main()
