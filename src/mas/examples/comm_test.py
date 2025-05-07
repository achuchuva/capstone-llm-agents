"""Test file for basic MAS"""

import random
from typing import Annotated, Callable
from app import App

from mas.ag2.ag2_agent import AG2MASAgent
from mas.ag2.ag2_task import AG2Task
from mas.base_resource import BaseResource
from mas.communication.checkpoint import Checkpoint
from mas.communication.communication_interface import CommunicationInterface
from mas.communication.decision_handlers.basic_decision_handler import (
    BasicDecisionHandler,
)
from mas.communication.decision_makers.basic_decision_maker import BasicDecisionMaker
from mas.communication.evaluators.basic_evaluator import BasicEvaluator
from mas.multi_agent_system import MultiAgentSystem
from mas.query.mas_query import MASQuery
from mas.resource_alias import ResourceAlias
from mas.resources.empty import EmptyResource
from mas.task import Task
from mas.tasks.write_sentence import SentenceResource, TopicResource
from utils.string_template import generate_str_using_template


def spoofed_error_generate_str(
    template_str: Annotated[str, "The template string to use."],
) -> Callable[[BaseResource], str]:

    # 50% chance to generate str using wrong template
    bad_template_str = "Respond with 'Error: Failed to get fact.'"

    if random.random() < 0.5:
        template_str = bad_template_str

    return generate_str_using_template(template_str)


def test_comm_proto_mas(app: App):
    """Test basic MAS."""

    alias = ResourceAlias()

    # add aliases
    alias.add_resource_alias("empty", EmptyResource)
    alias.add_resource_alias("sentence", SentenceResource)
    alias.add_resource_alias("topic", TopicResource)

    mas = MultiAgentSystem(alias)

    yaml_file = "./resource/example/number.yaml"

    mas_query = MASQuery.from_yaml(yaml_file)

    agent = AG2MASAgent(
        name="NumberAssistantAgent",
        description="You are an assistant that knows all about numbers.",
        llm_config=app.config_manager.get_llm_config(use_tools=False),
    )

    get_a_number_fact = AG2Task(
        name="GetNumberFact",
        description="Get a fact about a number.",
        input_resource=TopicResource,
        output_resource=SentenceResource,
        generate_str=spoofed_error_generate_str(
            "'{topic}'",
        ),
        agent=agent,
    )

    descriptor_mapping: dict[str, Task] = {
        "about_topic": get_a_number_fact,
    }

    # example tasks
    example_tasks: list[Task] = [
        # write a sentence about a topic
        get_a_number_fact,
    ]

    # add tasks to mas
    for task in example_tasks:
        mas.add_task(task)

    checkpoint = Checkpoint(agent)

    agent_interface = CommunicationInterface(
        handler=BasicDecisionHandler(checkpoint),
        evaluator=BasicEvaluator(),
        decision_maker=BasicDecisionMaker([]),
    )

    mas.add_agent(agent)

    mas.communication_protocol.add_agent_interface(agent, agent_interface)

    try:
        output_resources = mas.solve_query(mas_query, descriptor_mapping)
    except Exception as e:
        print("[AGENT]: I'm sorry, I can't help with that task.")
        return
    # print the output resources
    for output_resource in output_resources:
        json = output_resource.model.model_dump()

        sentence = json.get("sentence", None)

        print(f"[AGENT]: {sentence}")
