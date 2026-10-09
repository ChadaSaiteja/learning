from langchain_text_splitters import RecursiveCharacterTextSplitter

# Sample long text
text = """
# Order Installation Guide

## 1. Order Lifecycle

When a customer places an order, the order is first created in the ordering system. The order receives a unique order number that is used to track the order across different systems.

After the order is created, the order is sent to the Service Order Orchestration (SOO) system. SOO coordinates the order between Salesforce, Dynamics, and other downstream systems.

An order normally moves through several stages: Order Created, Validation, Pre-fielding, Installation Scheduled, Installation In Progress, and Installation Completed.

The exact sequence can vary depending on the type of service and whether the order has dependencies.

## 2. Pre-fielding

Pre-fielding is performed before the final installation appointment. During this stage, a technician or field team may need to verify the customer's address, network availability, equipment requirements, and other installation prerequisites.

If pre-fielding is required, the order may remain in the Pre-fielding state until the required work is completed.

Once pre-fielding is completed successfully, Dynamics sends an event indicating that the order is ready for the next stage.

The Salesforce system consumes this event and updates the corresponding order record. The event normally contains the work order number, order number, status, and event creation timestamp.

## 3. Installation Dependencies

Some installations cannot proceed until one or more dependencies are completed.

Examples of dependencies include Service Wire Center, Missing Drop, Damage Drop, Terminal Construction, and other infrastructure-related activities.

When an order has dependencies, Dynamics sends an Install Dependency event containing information about the dependencies associated with the work order.

A dependency may contain a dependency name, dependency case ID, dependency work order ID, external ID, and estimated resolution date.

If multiple dependencies exist, the Salesforce integration must identify the applicable dependencies before determining the expected installation date.

For Service Wire Center, Missing Drop, and Damage Drop dependencies, the latest estimated resolution date should be considered the dependency completion date.

For example, assume an order has three dependencies. Service Wire Center has an estimated resolution date of September 10, Missing Drop has an estimated resolution date of September 12, and Damage Drop has an estimated resolution date of September 9.

The dependency completion date should therefore be September 12 because it is the latest date among the applicable dependencies.

## 4. Multiple Dependency Events

An order may receive more than one Install Dependency event during its lifecycle.

For example, an initial event may contain a Service Wire Center dependency with an estimated resolution date of September 10.

Later, Dynamics may send another event containing a Missing Drop dependency with an estimated resolution date of September 15.

The integration should not assume that the first dependency event contains the complete list of dependencies.

When a new event is received, the integration should evaluate the dependency information provided by that event and determine whether the Salesforce Drop Commit Date needs to be updated.

If the latest applicable dependency date changes, Salesforce should be updated with the new date.

## 5. Salesforce Order Updates

The Salesforce Order record contains several fields that are populated based on events received from Dynamics.

The Drop Commit Date represents the expected date by which applicable drop-related dependencies are expected to be resolved.

When an Install Dependency event is received, the integration evaluates the dependencies and determines the maximum estimated resolution date for Service Wire Center, Missing Drop, and Damage Drop.

The resulting date is populated in the Drop_Commit_Date__c field on the Salesforce Order.

If a later event contains a newer estimated resolution date, the existing Drop_Commit_Date__c value should be updated.

If an event does not contain any applicable dependency, the integration should not overwrite a previously populated Drop_Commit_Date__c value with an empty value unless the business rules explicitly require it.

## 6. Installation Scheduling

After all required dependencies are completed, the order can proceed toward installation scheduling.

The installation appointment contains information such as appointment date, appointment start time, appointment end time, technician information, and service location.

When an installation is scheduled, Dynamics sends an event containing the appointment information.

Salesforce consumes the event and updates the order with the installation appointment details.

During rescheduling, the new appointment information should replace the previous appointment information.

The appointment start date and time are particularly important because they determine when the technician is expected to arrive at the customer's location.

If the appointment start date is missing from a rescheduling event, the integration should not blindly overwrite an existing appointment date with a null value.

## 7. Error Handling

Integration failures can occur when Salesforce receives an invalid event, when a downstream API is unavailable, or when required fields are missing from the event payload.

For example, an Install Dependency event may contain a work order number but no Salesforce Order ID.

In this situation, the integration should log the event and identify why the Salesforce order could not be located.

If a downstream API returns an error, the integration should capture the error code and message and make the failure available for investigation.

Transient errors such as network timeouts may be retried according to the integration retry policy.

Permanent errors, such as invalid order identifiers, should generally not be retried indefinitely.

## 8. Example End-to-End Scenario

Consider order ORD-123.

The order is created in Salesforce and sent to Dynamics for fulfillment.

Dynamics performs pre-fielding and sends a Pre-field Completed event.

Later, Dynamics sends an Install Dependency event containing the following dependencies:

- Service Wire Center — estimated resolution date: September 10
- Missing Drop — estimated resolution date: September 12
- Terminal Construction — estimated resolution date: September 20

The integration filters the dependencies according to the applicable business rules.

Terminal Construction is not included in the Drop Commit Date calculation.

The latest applicable dependency date is September 12, so Salesforce updates Drop_Commit_Date__c to September 12.

Two days later, Dynamics sends another Install Dependency event containing a Damage Drop dependency with an estimated resolution date of September 15.

The integration evaluates the new dependency information and determines that September 15 is now the latest applicable date.

Salesforce therefore updates Drop_Commit_Date__c from September 12 to September 15.

Once the dependencies are resolved, Dynamics schedules the installation for September 18 at 10:00 AM.

Salesforce receives the installation event and updates the order with the appointment information.

The order can then proceed through the normal installation lifecycle until the installation is completed.
"""

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=10)
texts = text_splitter.split_text(text)

print(texts)